

from .models import Book,BookInstance,Author,Language,Genre
from django.views import generic
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from catalog.forms import RenewBookForm
import datetime
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Author,Book
from catalog.forms import RenewBookForm

# Create your views here.
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    #-----available books----
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genre = Genre.objects.all().count()
    num_language = Language.objects.all().count()
    HarryP_books=''
    entry_list = list(Book.objects.filter(title__icontains='HARRY'))
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
   
   
    
    # for book in Book.objects.all():
    #     if 'HARRY'in book.title or 'Harry' in book.title:
    #         a.append(book.title)
    HarryP_books=','.join(a.title for a in entry_list)
    #b = ','.join(book.title for book in Book.objects.all())
  
    context={
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
        'num_genre':num_genre,
        'num_language':num_language,
        'HarryP_books':HarryP_books,
        'num_visits':num_visits,
  
      

    }
    return render(request,'index.html',context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book  

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

   

class AuthorDetailView(generic.DetailView):
    model = Author
    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['book_list'] = Book.objects.all()
        return context

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self) :
        return BookInstance.objects.filter(borrower = self.request.user).filter(status__exact ='o').order_by('due_back')


class AllBorrowedBooksListView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'catalog.can_view_all_books'
    model = BookInstance
    template_name = 'catalog/list_all_borrowed_books.html'
    paginate_by = 10
    

    def get_queryset(self) :
        return BookInstance.objects.filter(status__exact ='o')

@login_required
@permission_required('catalog.can_renew')
def renew_book_librarian(request,pk):
    book_instance = get_object_or_404(BookInstance,pk=pk)
    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date':proposed_renewal_date})

    context={
         'form': form,
         'book_instance':book_instance,
        }
    return render(request,'catalog/book_renew_librarian.html', context= context)


class AuthorCreate(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    login_url = 'login'
    permission_required ='catalog.can_renew'
    model = Author
    fields = ['first_name','last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death':'11/06/2020','date_of_birth':'2020-11-03'}


class AuthorUpdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = 'login'
    permission_required ='catalog.can_renew'
    model = Author
    fields = '__all__'
#create and update views will use the same template 'modelname_form.html'
# (in our eg:author_form.html )

class AuthorDelete(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = 'login'
    permission_required ='catalog.can_renew'
    model = Author
    success_url = reverse_lazy('author')
# delete view will check for the 'modelname_confirm_delete.html' template

class BookCreate(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    login_url = 'login'
    permission_required ='catalog.can_renew'
    model = Book
    fields =['title','author','summary','isbn','genre','language']

class BookUpdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = 'login'
    permission_required ='catalog.can_renew'
    model = Book
    fields = '__all__'
class BookDelete(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = 'login'
    permission_required ='catalog.can_renew'
    model = Book
    success_url = reverse_lazy('books')



