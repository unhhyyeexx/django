# pjt 08

> DB 설계를 활용한 REST API 설계



#### 🧐 T O D A Y

- DRF(Django Rest Framework)를 활용한 API Server 제작
- Database 1:N, M:N 에 대한 이해





## 🧱 개발도구 및 라이브러리

1. Visual Studio Code
2. Google Chrome Browser
3. Postman
4. Django 3.2.12 
   - pip install django==3.2.12





## 🔨 기본 틀 잡기

- 프로젝트 이름은 pjt08, 앱 이름은 movies

- **Models.py**

  ```python
  # movies/models.py
  
  from django.db import models
  
  class Actor(models.Model):
      name = models.CharField(max_length=100)
  
      def __str__(self):
          return self.name
  
  class Movie(models.Model):
      title = models.CharField(max_length=100)
      overview = models.TextField()
      release_date = models.DateTimeField()
      poster_path = models.TextField()
      actors = models.ManyToManyField(Actor, related_name='movies')
  
      def __str__(self):
          return self.title
  
  class Review(models.Model):
      title = models.CharField(max_length=100)
      content = models.TextField()
      movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
  
      def __str__(self):
          return self.title
  ```

- **urls.py**

  ```python
  # movies/urls.py
  
  from django.urls import path
  from . import views
  
  urlpatterns = [
      path('actors/', views.actor_list),
      path('actors/<int:actor_pk>/', views.actor_detail),
      path('movies/', views.movie_list),
      path('movies/<int:movie_pk>/', views.movie_detail),
      path('reviews/', views.review_list),
      path('reviews/<int:review_pk>/', views.review_detail),
      path('movies/<int:movie_pk>/reviews/', views.create_review),
  ]
  ```

  



## 🌎 serializers

- model과 form을 사용해서 앱 어플리케이션을 만들었었는데, 이번주는 serializer를 이용해서 api server를 제작하였다.

### 1️⃣ actors.py

```python
from rest_framework import serializers
from .movie import MovieForeign
from ..models import Actor

class ActorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = '__all__'

class ActorSerializer(serializers.ModelSerializer):
    movies = MovieForeign(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = ('id', 'movies', 'name',)
```

### 2️⃣ movies.py

```python
from rest_framework import serializers
from ..models import Movie, Actor
from .review import ReviewListSerializer

class MovieListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ('title', 'overview',)

class MovieSerializer(serializers.ModelSerializer):

    class Actor(serializers.ModelSerializer):
        class Meta:
            model = Actor
            fields = ('name',)
    actors = Actor(read_only=True, many=True)
    review_set = ReviewListSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ('id', 'actors', 'review_set', 'title', 'overview', 'release_date', 'poster_path')
        read_only_fields = ('movie',)

class MovieForeign(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title',)
```

### 3️⃣ review.py

```python
from rest_framework import serializers
from ..models import Movie, Review

class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('title', 'content', )

class ReviewSerializer(serializers.ModelSerializer):
    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('title',)
    movie = MovieSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ('id', 'movie', 'title','content',)
```





## 🌟 response result

### 1️⃣ Actor List (GET api/v1/actors/)

![1](README-%EC%95%84%ED%98%84.assets/1-16506148874501.PNG)



### 2️⃣ Actor Detail (GET api/v1/actors/1/)

![2](README-%EC%95%84%ED%98%84.assets/2-16506149616472.PNG)



### 3️⃣ Movie List (GET api/v1/movies/)

![3](README-%EC%95%84%ED%98%84.assets/3-16506149986353.PNG)





### 4️⃣ Movie Detail (GET api/v1/movies/1/)

![4](README-%EC%95%84%ED%98%84.assets/4-16506150851474-16506150905035.PNG)



### 5️⃣ Review List (GET api/v1/reviews/)

![5](README-%EC%95%84%ED%98%84.assets/5-16506151273276.PNG)





### 6️⃣ Review Detail (GET api/v1/reviews/1/)

![6](README-%EC%95%84%ED%98%84.assets/6-16506151558887.PNG)



### 7️⃣ POST api/v1/movies/1/reviews/

![7](README-%EC%95%84%ED%98%84.assets/7-16506151875868.PNG)



### 8️⃣ PUT api/v1/reviews/1/

![8](README-%EC%95%84%ED%98%84.assets/8-16506152076609.PNG)



### 9️⃣ DELETE api/v1/reviews/1/

![9](README-%EC%95%84%ED%98%84.assets/9-165061524919510.PNG)





## 💫 마무리

#### 오늘 내 실수들 + 배운 것들

- 오늘은 Django REST framework(DRF) 라이브러리를 사용한 JSON응답으로 api server를 구성해보았다. 장고에서는 ModelForm을 이용해서 HTML응답을 받는다면, DRF에서는 Serializer를 이요해서 JSON응답을 받는다. 직렬화라는 개념이 생소하기도 하고 실습을 많이 해보지 않아서 어려웠지만, 페어와 함께 나름 빠르게 pjt를 진행했다😎

- Serializer는 장고의 Form이나 ModelForm 클래스랑 매우 유사하게 구성되고 작동하기 때문에 초반에는 큰 어려움이 없이 코드를 짰다. 후반에 가서 명세와 비교하며 디테일을 맞추는 과정에서 오류를 발견했는데, movie 데이터에 들어있는 actor가 딕셔너리 타입이고, 나는 그 actor에서 'name'이란 field만 빼오고 싶었는데, 그게 잘 구성이 되지 않았다. 처음에는 actor에 외래키를 써서 가져오는 방법으로 코드를 짰는데, 이게 actor와 movie, review가 다 참조관계에 있고, 각 데이터에 같은 이름의 field가 있어서 순환오류(?)(circular오류?)가 나는 것 같았다. 

- 위 오류의 해결 방법은 다음과 같다.

  ```python
  #movie/serializers/review.py/ReviewSerializer
  
  class ReviewSerializer(serializers.ModelSerializer):
      class MovieSerializer(serializers.ModelSerializer):
          class Meta:
              model = Movie
              fields = ('title',)
      movie = MovieSerializer(read_only=True)
      class Meta:
          model = Review
          fields = ('id', 'movie', 'title','content',)
  ```

  위 코드 예시는 해당 리뷰의 영화정보 중 제목만 가져오도록 만든 클래스이다. 클래스 안에서 필요한 field를 구할 수 있는 클래스를 위에 선언해주고 해당 변수를 field로 가져오면 된다.

- 나름 수월하고 재밌게 진행했던 pjt였다. api server 구축이라는 말에 겁먹고 으 하기싫어 했는데 생각보다 소질이 있을지도..? 다음주부터 자바스크립트랑 뷰를 공부하는데 빨리 배운 걸 종합해서 최종 pjt를 해보고싶다는 생각이 들었다 😏







