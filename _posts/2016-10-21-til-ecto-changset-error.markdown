---
layout: post
title:  "[TIL] Ecto changset errors"
date: 2016-10-21 14:08:00 +0700
categories: ecto
---

Ở Controller ta có
{% highlight elixir %}
changeset = Ecto.Changeset.add_error(changeset, :email, "Email doesn't exist in DB. Please contact admin")
{% endhighlight %}

Còn ở view:

{% highlight elixir %}
<%= form_for @changeset, user_path(@conn, :send_info), [method: :post], fn f -> %>
  <%= if f.errors != [] %>
    <div class="alert alert-danger">
      <p>Oops, something went wrong! Please check the errors below:</p>
    </div>
  <% end %>

  <div class="form-group">
    <label>Email</label>
    <%= email_input f, :email, class: "form-control" %>
    <%= error_tag f, :email %>
  </div>
  <div class="form-group">

  <div class="form-group">
    <%= submit "Request", class: "btn btn-primary" %>
  </div>
<% end %>
{% endhighlight %}

Lúc đầu cứ tưởng đúng, nhưng kết quả là khi lỗi không thấy error hiện ra ???
Hoá ra là, `form_for` sẽ kiểm tra `action` của `changeset`: có hành động nào đang được thực hiện.
Nếu có mới thêm lỗi. Đó là lí do ta phải check `<% if @changeset.action %>`. Vậy add error là chưa đủ, phải set `action` nữa:

{% highlight elixir %}
changeset = Ecto.Changeset.add_error(changeset, :email, "Email doesn't exist in DB. Please contact admin")
changeset = %{changeset | action: :request}
{% endhighlight %}
