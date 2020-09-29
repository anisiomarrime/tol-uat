import random
import string
import uuid
from _md5 import md5
from datetime import datetime
from time import localtime

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.defaultfilters import slugify
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from validate_email import validate_email
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import cloudinary
import cloudinary.uploader
import cloudinary.api
import uuid
import sendgrid
import os

from dashboard.forms import FormPost, FormRegister, FormLogin, FormPasswordRecover
from dashboard.models import Category, City, Package, Seller, Post, Payment, UpdateRequest, Photo, Doc, UserTokens
from django.contrib import messages

cloudinary.config(
            cloud_name="soboladas",
            api_key="389966337797351",
            api_secret="iVtQsRUiDbxWKPDZFy4T9aUt1UY"
        )


def sendEmail(msg, subject, to):
    mensagem = Mail(from_email='noreply@tol.co.mz',to_emails=to, subject=subject,html_content=msg)
    try :
        sg = SendGridAPIClient('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')
        response = sg.send(mensagem)
        return response.status_code
    except Exception as e:
        print('error: ')
        print(e)
        return 500


def upload_doc(photo, filename):
    random_test = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    file_name = "soboladas-" + slugify(filename) + "-" + random_test
    try:
        cloudinary.uploader.upload(photo, folder="soboladas/docs/", public_id=file_name,
                                   overwrite=True,
                                   quality=90,
                                   resource_type="image")
    except Exception as e:
        file_name = None
    return file_name


def upload_photo(photo, filename):
    random_test = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    file_name = "soboladas-" + slugify(filename) + "-" + random_test
    try:
        cloudinary.uploader.upload(photo, folder="soboladas/anuncios/", public_id=file_name,
                                   overwrite=True,
                                   quality=100,
                                   resource_type="image")
    except Exception as e:
        file_name = None
    return file_name


def upload_profile(photo, filename):
    random_test = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    file_name = "soboladas-" + slugify(filename) + "-" + random_test
    try:
        cloudinary.uploader.upload(photo, folder="soboladas/profiles/", public_id=file_name,
                                   overwrite=True,
                                   quality=90,
                                   resource_type="image")
    except Exception as e:
        print(e)
        file_name = None
    return file_name


def total_posts_today(seller):
    posts_today = 0
    posts = Post.objects.filter(seller=seller)
    for post in posts:
        if post.created_at.date() == datetime.today().date():
            posts_today = posts_today + 1
    return posts_today


class IndexTemplateView(TemplateView):
    template_name = "index.html"
    context_object_name = "index"

    def get_context_data(self, filter=None, **kwargs):
        context = super(IndexTemplateView, self).get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/dashboard/login/')

        context = IndexTemplateView.get_context_data(self, **kwargs)
        seller = Seller.objects.get(user=request.user)
        context['seller'] = seller
        context['posts_today'] = total_posts_today(seller)

        if request.user.is_staff:
            context['nr_posts'] = Post.objects.count()
            context['is_admin'] = True
        else:
            context['nr_posts'] = Post.objects.filter(seller=seller).count()
        return render(request, 'index.html', context)


class PostAddTemplateView(TemplateView):
    template_name = "post_add.html"
    context_object_name = "post_add"

    def get_context_data(self, **kwargs):
        context = super(PostAddTemplateView, self).get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/dashboard/login/')

        context = PostAddTemplateView.get_context_data(self, **kwargs)

        if request.user.is_staff:
            context['is_admin'] = True

        context['categories'] = Category.objects.all()
        context['seller'] = Seller.objects.get(user=request.user)
        return render(request, 'post_add.html', context)

    def post(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/dashboard/login/')

        form = FormPost(request.POST)
        seller = Seller.objects.get(user=request.user)
        context = PostAddTemplateView.get_context_data(self, **kwargs)

        if request.user.is_staff:
            context['is_admin'] = True

        if total_posts_today(seller) < seller.package.max_posts:
            if form.is_valid():
                text_rand = "".join(random.choice(string.ascii_lowercase) for i in range(10))
                data = form.data
                category = Category.objects.get(id=int(data['category']))
                post = Post.objects.create(seller=seller, category=category, title=str(data['title']).title(),
                                    description=data['description'], slug=slugify(data['title']+"-"+text_rand), price=data['price'].replace(' ', ''))

                photo1 = upload_photo(form.data['photo1'], data['title'])

                if not None == photo1:
                    post.thumb = photo1+".jpg"
                    Photo.objects.create(post=post, photo=photo1 + ".jpg")
                    photo2 = upload_photo(form.data['photo2'], data['title'])

                if not None == photo2:
                    Photo.objects.create(post=post, photo=photo2+".jpg")
                    photo3 = upload_photo(form.data['photo3'], data['title'])

                    if not None == photo3:
                        Photo.objects.create(post=post, photo=photo3+".jpg")

                post.save()

                context['message'] = 'Anúncio registado com sucesso, em breve estará visível no site!'
        else:
            context['message'] = 'Você já atingiu o limite de {0} posts por dia, tente novamente amanhã.'.format(seller.package.max_posts)

        context['categories'] = Category.objects.all()
        context['seller'] = seller
        return render(request, 'post_add.html', context)

    def edit(request, id):
        post = Post.objects.get(id=int(id))
        context = {}
        if request.user.is_staff:
            context['is_admin'] = True

        context['post'] = post
        context['seller'] = post.seller
        context['categories'] = Category.objects.all()

        if request.method == 'POST':
            form = FormPost(request.POST)
            if form.is_valid():
                data = form.data
                post.title = str(data['title']).title()
                post.description = data['description']
                post.price = data['price'].replace(' ', '')
                post.category = Category.objects.get(id=int(data['category']))
                post.save()
                context['message'] = 'Anúncio actualizado com sucesso!'
            else:
                context['message'] = 'Não foi possível actualizar o anúncio, por favor preencha devidamente os campos!'

        return render(request, 'post_add.html', context)


class PostListTemplateView(TemplateView):
    template_name = "post_list.html"
    context_object_name = "post_list"

    @csrf_exempt
    def approve(request, id):
        if request.user.id:
            post = Post.objects.get(id=int(id))
            if post.status == 0:
                post.status = 1
                post.save()
            return JsonResponse({'status': 'success'}, status=200)
        return JsonResponse({'status': 'Not allowed'}, status=403)

    @csrf_exempt
    def remove(request, id):
        if request.user.id:
            post = Post.objects.get(id=int(id))
            post.status = 3
            post.save()
            return JsonResponse({'status': 'success'}, status=200)
        return JsonResponse({'status': 'Not allowed'}, status=403)

    def get_context_data(self, filter=None, **kwargs):
        context = super(PostListTemplateView, self).get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/dashboard/login/')

        context = PostListTemplateView.get_context_data(self, **kwargs)
        seller = Seller.objects.get(user=request.user)
        context['seller'] = seller

        if request.user.is_staff:
            context['posts'] = Post.objects.all()
            context['is_admin'] = True
        else:
            context['posts'] = Post.objects.filter(seller=seller)
        return render(request, 'post_list.html', context)


class LoginTemplateView(TemplateView):
    template_name = "login.html"
    context_object_name = "login"

    def get_context_data(self, **kwargs):
        context = super(LoginTemplateView, self).get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        context = LoginTemplateView.get_context_data(self, **kwargs)
        return render(request, LoginTemplateView.template_name, context)

    def post(self, request, **kwargs):
        form = FormLogin(request.POST)
        context = LoginTemplateView.get_context_data(self, **kwargs)

        if form.is_valid():
            user = authenticate(username=form.data['username'], password=form.data['password'])

            if user is not None:
                login(request, user)
                return redirect('/dashboard/')
            else:
                messages.info(request, 'Username or Password inválido!!')
                # context['message'] = 'Username or Password Incorrect!!'
        else:
            messages.info(request, 'Por favor, preencha devidamente os campos.')

        return render(request, LoginTemplateView.template_name, {'form': form})


class LogoutTemplateView(TemplateView):
    template_name = "login.html"
    context_object_name = "login"

    def get(self, request, **kwargs):
        logout(request)
        return redirect('/dashboard/login/')

class ChangePasswordTemplateView(TemplateView):
    template_name = "change_password.html"
    context_object_name = "change_password"

    def get_context_data(self, **kwargs):
        context = super(ChangePasswordTemplateView, self).get_context_data(**kwargs)
        return context

    def post(self, request, **kwargs):
        form = FormPasswordRecover(request.POST)
        context = ChangePasswordTemplateView.get_context_data(self, **kwargs)

        if form.is_valid():
            data = form.data
            userToken = UserTokens.objects.get(token=request.GET['token'])
            user = userToken.user
            # user.password = data['password']
            user.set_password(data['password'])
            user.save()
            return redirect('/dashboard/login/')
        else:
            return redirect('/dashboard/login/')


class ForgotPasswordTemplateView(TemplateView):
    template_name = "forgot_password.html"
    context_object_name = "forgot_password"

    def get_context_data(self, **kwargs):
        context = super(ForgotPasswordTemplateView, self).get_context_data(**kwargs)
        return context

    def post(self, request, **kwargs):
        if validate_email(request.POST['email']):
            try:
                gerador= uuid.uuid4()
                UserTokens.objects.create(user=User.objects.get(email=request.POST['email']), token = gerador)
                message = Mail(
                    from_email='noreply@tol.co.mz',
                    to_emails=request.POST['email'],
                    subject='Mudar Password',
                    html_content='<strong>'+'Clique o link para mudar a password : href=https://www.tol.co.mz/dashboard/change_password/?token='+str(gerador)+'+</strong>')
                try:
                    sg = SendGridAPIClient('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')
                    response = sg.send(message)
                    print(response.status_code)
                    print(response.body)
                    print(response.headers)
                except Exception as e:
                    print(e)
                return redirect('/dashboard/login/')
            except Exception as e:
                messages.info(request, 'Email Inválido!')
                return render(request, ForgotPasswordTemplateView.template_name)
        else :
            messages.info(request, 'Email Inválido!')
            return redirect('/dashboard/forgot_password')


class RegisterTemplateView(TemplateView):
    template_name = "register.html"
    context_object_name = "register"

    def get_context_data(self, **kwargs):
        context = super(RegisterTemplateView, self).get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        context = RegisterTemplateView.get_context_data(self, **kwargs)
        context['cities'] = City.objects.all()
        return render(request, RegisterTemplateView.template_name, context)

    def post(self, request, **kwargs):
        form = FormRegister(request.POST)
        context = RegisterTemplateView.get_context_data(self, **kwargs)

        if form.is_valid():
            data = form.data
            if validate_email(data['email']):
                try:
                    User.objects.get(email=data['email'])
                    context['message'] = 'Já existe uma conta com este e-mail.'
                except:
                    user = User.objects.create_user(email=data['email'], username=data['email'],
                                                    password=data['password'],
                                                    is_active=True)

                    name = str(data['name']).split(' ')
                    user.first_name = name[0]
                    user.last_name = name[-1]
                    city = City.objects.get(id=int(data['province']))
                    package = Package.objects.get(id=1)

                    Seller.objects.create(user=user, city=city, package=package, mobile=data['mobile'])
                    user.save()

                    return redirect('/dashboard/login/')
            else:
                context['message'] = 'Por favor, informe um e-mail válido.'
        else:
            context['message'] = 'Por favor, preencha devidamente os campos.'

        context['cities'] = City.objects.all()
        return render(request, RegisterTemplateView.template_name, context)


class ProfileTemplateView(TemplateView):
    template_name = "profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super(ProfileTemplateView, self).get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/dashboard/login/')

        try:
            is_doc = int(request.GET['doc']) == 1
        except:
            is_doc = True

        context = ProfileTemplateView.get_context_data(self, **kwargs)
        if request.user.is_staff:
            context['is_admin'] = True

        seller = Seller.objects.get(user=request.user)

        try:
            doc = Doc.objects.get(seller=seller)
            seller.doc = doc.photo
        except:
            seller.doc = ''

        context['cities'] = City.objects.all()
        context['is_doc'] = is_doc
        context['seller'] = seller
        return render(request, ProfileTemplateView.template_name, context)

    def post(self, request, **kwargs):
        context = ProfileTemplateView.get_context_data(self, **kwargs)
        seller = Seller.objects.get(user=request.user)

        if request.user.is_staff:
            context['is_admin'] = True

        is_doc = int(request.GET['doc']) == 1

        if is_doc:
            docs = Doc.objects.filter(seller=seller, approved=False)
            if len(docs) >= 1:
                context['message'] = 'O documento já foi, por favor aguarde pela aprovação!'
            else:
                file_names = upload_doc(request.POST['doc'], seller.user.first_name)
                Doc.objects.create(photo=file_names, seller=seller)
                context['message'] = 'Documento enviado com sucesso, por favor aguarde pela aprovação!'
        else:
            form = FormRegister(request.POST)
            if form.is_valid():
                data = form.data

                seller.mobile = data['mobile']
                seller.mobile_alternative = data['mobile_alternative']
                seller.address = data['address']
                seller.city = City.objects.get(id=int(data['province']))

                user = User.objects.get(id=seller.user.id)
                name = str(data['name']).split(' ')
                user.first_name = name[0]
                user.last_name = str(data['name']).replace(name[0], "").strip()

                try:
                    res = upload_profile(data['photo'], name)
                    if not None == res:
                        seller.photo = res
                except:
                    pass

                seller.save()
                user.save()

                context['message'] = 'Dados actualizados com sucesso!'
            else:
                context['message'] = 'Por favor, preencha devidamente os campos.'

        seller = Seller.objects.get(id=seller.id)

        try:
            doc = Doc.objects.get(seller=seller)
            seller.doc = doc.photo
        except:
            seller.doc = ''

        context['cities'] = City.objects.all()
        context['seller'] = seller
        context['is_doc'] = not is_doc
        return render(request, ProfileTemplateView.template_name, context)


class SellerListTemplateView(TemplateView):
    template_name = "seller_list.html"
    context_object_name = "seller_list"

    @csrf_exempt
    def staff(request, id):
        if request.user.id:
            seller = Seller.objects.get(id=int(id))
            user = User.objects.get(id=seller.user.id)
            if user.is_staff == 0:
                user.is_staff = 1
                user.save()
            return JsonResponse({'status': 'success'}, status=200)
        return JsonResponse({'status': 'Not allowed'}, status=403)

    @csrf_exempt
    def doc(request, id):
        if request.user.id:
            seller = Seller.objects.get(id=int(id))
            seller.is_verified = True
            seller.save()
            return JsonResponse({'status': 'success'}, status=200)
        return JsonResponse({'status': 'Not allowed'}, status=403)

    @csrf_exempt
    def profile(request):
        if request.user.id:
            seller = Seller.objects.get(user=request.user)
            try:
                cloudinary.uploader.destroy(public_id=seller.photo, invalidate=True, folder="soboladas/anuncios/")
                seller.photo = 'admin.jpg'
                seller.save()
            except Exception as e:
                return JsonResponse({'status': 'error ao remover photo'}, status=500)
            return JsonResponse({'status': 'success'}, status=200)
        return JsonResponse({'status': 'Not allowed'}, status=403)

    def get_context_data(self, filter=None, **kwargs):
        context = super(SellerListTemplateView, self).get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/dashboard/login/')

        if not request.user.is_staff:
            return redirect('/dashboard/')

        context = SellerListTemplateView.get_context_data(self, **kwargs)
        sellers = Seller.objects.all()
        seller = Seller.objects.get(user=request.user)

        for sell in sellers:
            try:
                sell.doc = Doc.objects.get(seller=sell).photo
                sell.doc = "https://res.cloudinary.com/soboladas/image/upload/v1588360230/soboladas/docs/" + sell.doc + ".jpg"
            except:
                sell.doc = ''
            sell.total_posts = Post.objects.filter(seller=sell).count()

        context['seller'] = seller
        context['sellers'] = sellers
        context['is_admin'] = True

        return render(request, 'seller_list.html', context)


class PaymentsTemplateView(TemplateView):
    template_name = "payments.html"
    context_object_name = "payments"

    def get_context_data(self, filter=None, **kwargs):
        context = super(PaymentsTemplateView, self).get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/dashboard/login/')

        if not request.user.is_staff:
            return redirect('/dashboard/')

        context = PaymentsTemplateView.get_context_data(self, **kwargs)
        seller = Seller.objects.get(user=request.user)

        context['seller'] = seller
        context['payments'] = Payment.objects.all()
        context['is_admin'] = True

        return render(request, 'payments.html', context)


class RequestsTemplateView(TemplateView):
    template_name = "requests.html"
    context_object_name = "requests"

    def get_context_data(self, filter=None, **kwargs):
        context = super(RequestsTemplateView, self).get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/dashboard/login/')

        if not request.user.is_staff:
            return redirect('/dashboard/')

        context = RequestsTemplateView.get_context_data(self, **kwargs)
        seller = Seller.objects.get(user=request.user)

        context['seller'] = seller
        context['requests'] = UpdateRequest.objects.all()
        context['is_admin'] = True

        return render(request, 'requests.html', context)

    @csrf_exempt
    def upgrade(request):
        if request.user.id:
            seller = Seller.objects.get(user__id=request.user.id)
            try:
                UpdateRequest.objects.get(seller=seller)
            except:
                UpdateRequest.objects.create(seller=seller)
            return JsonResponse({'status': 'success'}, status=200)
        return JsonResponse({'status': 'Not allowed'}, status=403)


class PlansTemplateView(TemplateView):
    template_name = "plans.html"
    context_object_name = "plans"

    def get_context_data(self, filter=None, **kwargs):
        context = super(PlansTemplateView, self).get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/dashboard/login/')

        context = PlansTemplateView.get_context_data(self, **kwargs)
        seller = Seller.objects.get(user=request.user)

        if request.user.is_staff:
            context['is_admin'] = True

        context['seller'] = seller
        context['packages'] = Package.objects.all()

        return render(request, 'plans.html', context)

