---
title: Anglican News 
layout: default
---

  <div>
<ul>
  {% for post in site.posts %}
    <li>
      <a href="/anglican/{{ post.url }}">{{ post.date | date_to_string }} : {{ post.title }}</a>
      <p>{{ post.excerpt }}</p>
    </li>
  {% endfor %}
</ul>
  </div>
