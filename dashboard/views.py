from accounts.decorators import admin_required
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import User
from .forms import UserForm
from categories.models import Category
from products.models import Product
from django.core.paginator import Paginator
from orders.models import Order
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.contrib import messages
from chatbot.models import ChatHistory
from django.db.models import Count
from django.db.models.functions import TruncDate
import json
User = get_user_model()

@admin_required
def dashboard(request):
    products = Product.objects.select_related("category").order_by("-id")

    keyword = request.GET.get("keyword")

    if keyword:
        products = products.filter(name__icontains=keyword)

    category_id = request.GET.get("category")

    if category_id:
        products = products.filter(category_id=category_id)
    paginator = Paginator(products, 10)
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)
    context = {
    "product_count": Product.objects.count(),
    "category_count": Category.objects.count(),

    "order_count": Order.objects.count(),

    "user_count": User.objects.count(),

    "completed_order_count": Order.objects.filter(
        status="completed"
    ).count(),

    "revenue": (
        Order.objects.filter(status="completed")
        .aggregate(total=Sum("total_price"))["total"]
        or 0
    ),

    "products": products,
    "categories": Category.objects.all(),
    "keyword": keyword,
    "selected_category": category_id,
}

    return render(
        request,
        "dashboard/index.html",
        context,
    )

@admin_required
def category_list(request):
    categories = Category.objects.all().order_by("id")

    return render(
        request,
        "dashboard/category_list.html",
        {
            "categories": categories,
        },
    )


@admin_required
def add_category(request):

    if request.method == "POST":

        from django.utils.text import slugify
        from django.utils.encoding import force_str

        name = request.POST.get("name")

        Category.objects.create(
            name=name,
            slug=slugify(force_str(name), allow_unicode=True),
        )

        return redirect("category_list")

    return render(request, "dashboard/add_category.html")
@admin_required
def edit_category(request, pk):

    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":

        from django.utils.text import slugify
        from django.utils.encoding import force_str

        category.name = request.POST.get("name")
        category.slug = slugify(force_str(category.name), allow_unicode=True)

        category.save()

        return redirect("category_list")

    return render(
        request,
        "dashboard/edit_category.html",
        {
            "category": category,
        },
    )
@admin_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        category.delete()
        return redirect("category_list")

    return render(
        request,
        "dashboard/delete_category.html",
        {
            "category": category,
        },
    )
@admin_required
def order_list(request):

    orders = Order.objects.select_related("user").order_by("-created_at")

    return render(
        request,
        "dashboard/order_list.html",
        {
            "orders": orders,
        },
    )


@admin_required
def update_order_status(request, pk):

    order = get_object_or_404(Order, pk=pk)

    if request.method == "POST":

        order.status = request.POST.get("status")

        order.save()

        return redirect("order_list")

    return render(
        request,
        "dashboard/update_order_status.html",
        {
            "order": order,
            "status_choices": Order.STATUS_CHOICES,
        },
    )
@admin_required
def order_detail(request, pk):

    order = get_object_or_404(
        Order.objects.select_related("user"),
        pk=pk
    )

    items = order.items.select_related("product")

    return render(
        request,
        "dashboard/order_detail.html",
        {
            "order": order,
            "items": items,
        },
    )
@admin_required
def add_user(request):

    if request.method=="POST":

        form=UserForm(request.POST)

        if form.is_valid():

            user=form.save(commit=False)

            password=request.POST.get("password")

            if password:
                user.set_password(password)

            else:
                user.set_password("123456")

            user.save()

            return redirect("user_list")

    else:

        form=UserForm()

    return render(request,"dashboard/add_user.html",{

        "form":form

    })
@admin_required
def delete_user(request,pk):

    user=get_object_or_404(User,pk=pk)

    if request.method=="POST":

        user.delete()

        return redirect("user_list")

    return render(request,"dashboard/delete_user.html",{

        "delete_user":user

    })
@admin_required
def staff_list(request):

    staffs = User.objects.filter(role="staff").order_by("-id")

    return render(request,"dashboard/staff_list.html",{

        "staffs":staffs

    })
@admin_required
def add_staff(request):

    if request.method=="POST":

        data = request.POST.copy()
        data["role"] = "staff"
        data["is_active"] = True

        form = UserForm(data)

        if form.is_valid():

            staff=form.save(commit=False)

            staff.role="staff"

            password=request.POST.get("password")

            if password:

                staff.set_password(password)

            else:

                staff.set_password("123456")

            staff.save()

            return redirect("staff_list")

    else:

        form=UserForm()

    return render(request,"dashboard/add_staff.html",{

        "form":form

    })
@admin_required
def user_list(request):

    users = User.objects.order_by("-id")

    return render(
        request,
        "dashboard/user_list.html",
        {
            "users": users
        }
    )


@admin_required
def edit_user(request, pk):

    user = get_object_or_404(
        User,
        pk=pk
    )

    if request.method == "POST":

        user.role = request.POST.get("role")

        user.is_active = (
            request.POST.get("is_active") == "1"
        )

        user.save()

        messages.success(
            request,
            "Cập nhật tài khoản thành công."
        )

        return redirect("user_list")

    return render(
        request,
        "dashboard/edit_user.html",
        {
            "user": user
        }
    )
@admin_required
def edit_staff(request, pk):
    staff = get_object_or_404(User, pk=pk, role="staff")

    if request.method == "POST":
        data = request.POST.copy()
        data["role"] = "staff"

        form = UserForm(data, instance=staff)

    if form.is_valid():
        staff = form.save(commit=False)
        staff.role = "staff"
        staff.is_active = request.POST.get("is_active") == "1"
        staff.save()

        messages.success(request, "Cập nhật nhân viên thành công.")
        return redirect("staff_list")
    else:
        form = UserForm(instance=staff)

    return render(
        request,
        "dashboard/edit_staff.html",
        {
            "form": form,
            "staff": staff,
        },
    )
@admin_required
def delete_staff(request, pk):
    staff = get_object_or_404(User, pk=pk, role="staff")

    if request.method == "POST":
        staff.delete()
        messages.success(request, "Xóa nhân viên thành công.")
        return redirect("staff_list")

    return render(
        request,
        "dashboard/delete_staff.html",
        {
            "staff": staff,
        },
    )
@admin_required
def chatbot_dashboard(request):
    
    chats = ChatHistory.objects.select_related(
        "user",
        "product",
    ).order_by("-created_at")

    keyword = request.GET.get("keyword")

    if keyword:
        chats = chats.filter(
            message__icontains=keyword
        )

    paginator = Paginator(chats, 15)

    page = request.GET.get("page")

    chats = paginator.get_page(page)

    top_products = (
        ChatHistory.objects
        .filter(product__isnull=False)
        .values("product__name")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    top_users = (
        ChatHistory.objects
        .values("user__username")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )
    product_labels = [
        item["product__name"]
        for item in top_products
]

    product_values = [
        item["total"]
        for item in top_products
]

    user_labels = [
        item["user__username"]
        for item in top_users
]

    user_values = [
        item["total"]
        for item in top_users
]
    context = {
        
        "chat_count": ChatHistory.objects.count(),

        "user_chat_count": (
            ChatHistory.objects
            .values("user")
            .distinct()
            .count()
        ),

        "top_products": top_products,

        "top_users": top_users,

        "chats": chats,

        "keyword": keyword,
        "product_labels": json.dumps(product_labels),
        "product_values": product_values,
        "user_labels": user_labels,
        "user_labels": json.dumps(user_labels),

    }

    return render(
        request,
        "dashboard/chatbot.html",
        context,
    )
@admin_required
def chatbot_report(request):

    daily_chats = (
        ChatHistory.objects
        .annotate(date=TruncDate("created_at"))
        .values("date")
        .annotate(total=Count("id"))
        .order_by("date")
    )

    labels = []
    values = []

    for item in daily_chats:

        labels.append(item["date"].strftime("%d/%m"))

        values.append(item["total"])

    context = {

        "labels": json.dumps(labels),

        "values": values,

        "chat_count": ChatHistory.objects.count(),

        "user_count": (
            ChatHistory.objects
            .values("user")
            .distinct()
            .count()
        ),

        "top_products": (
            ChatHistory.objects
            .filter(product__isnull=False)
            .values("product__name")
            .annotate(total=Count("id"))
            .order_by("-total")[:10]
        ),

        "top_users": (
            ChatHistory.objects
            .values("user__username")
            .annotate(total=Count("id"))
            .order_by("-total")[:10]
        ),

    }

    return render(
        request,
        "dashboard/chatbot_report.html",
        context,
    )