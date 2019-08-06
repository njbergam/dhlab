<script src="https://apis.google.com/js/platform.js" async defer></script>
<meta name="google-signin-client_id" content="750697789107-aq2vh0l8n3e86qpnhh89rmr6ptrrgfh4.apps.googleusercontent.com">
{% extends 'layout.html' %}

{% block body %}
<div class="g-signin2" data-onsuccess="onSignIn"></div>
<div class="container">
  <br style = "line-height:5">
  <h1>Ninth Grade </h1>
  <br style = "line-height:5">
  <div class="row">
  {% for text in ninthTexts %}
    <div class="col-sm-4">
      <div class="card">
        <img class="card-img-top" src={{text.image}} width="100" height="300" alt="Card image cap">
        <div class="card-body" style="height:10.5rem">
          <h5 class="card-title">{{text.title}}</h5>
          <p class="card-text">{{text.author}}</p>
          <a href="/downloadbooks/{{text.txtName}}" class="btn btn-primary" download={{text.txtName}} download >TXT</a>
          &nbsp
          &nbsp
          &nbsp
          &nbsp
          <a href="/downloadbooks/{{text.pdfName}}" class="btn btn-primary" download={{text.pdfName}} download >PDF</a>
        </div>
      </div>
    </div>
  {% endfor %}
  </div>
  <br style = "line-height:5">
  <hr size="50">
</div>




<div class="container">
  <br style = "line-height:5">
  <h1>Tenth Grade </h1>
  <br style = "line-height:5">
  <div class="row">
  {% for text in tenthTexts %}
    <div class="col-sm-4">
      <div class="card">
        <img class="card-img-top" src={{text.image}} width="100" height="300" alt="Card image cap">
        <div class="card-body" style="height:10.5rem">
          <h5 class="card-title">{{text.title}}</h5>
          <p class="card-text">{{text.author}}</p>
          <a href="/downloadbooks/{{text.txtName}}" class="btn btn-primary" download={{text.txtName}} download >TXT</a>
          &nbsp
          &nbsp
          &nbsp
          &nbsp
          <a href="/downloadbooks/{{text.pdfName}}" class="btn btn-primary" download={{text.pdfName}} download >PDF</a>
        </div>
      </div>
    </div>
  {% endfor %}
  </div>
  <br style = "line-height:5">
  <hr size="50">
</div>

<div class="container">
  <br style = "line-height:5">
  <h1>Eleventh Grade </h1>
  <br style = "line-height:5">
  <div class="row">
  {% for text in eleventhTexts %}
    <div class="col-sm-4">
      <div class="card">
        <!--<img class="card-img-top" src={{text.image}} width="100" height="300" alt="Card image cap">-->
        <div class="card-body" style="height:10.5rem">
          <h5 class="card-title">{{text.title}}</h5>
          <p class="card-text">{{text.author}}</p>
          <a href="/downloadbooks/{{text.txtName}}" class="btn btn-primary" download={{text.txtName}} download >TXT</a>
          &nbsp
          &nbsp
          &nbsp
          &nbsp
          <a href="/downloadbooks/{{text.pdfName}}" class="btn btn-primary" download={{text.pdfName}} download >PDF</a>
        </div>
      </div>
    </div>
  {% endfor %}
  </div>
  <br style = "line-height:5">
  <hr size="50">
</div>


{% endblock %}
