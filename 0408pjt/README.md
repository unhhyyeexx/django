# pjt 06

> DB를 활용한 웹 페이지 구현



#### 🧐 T O D A Y

- 오늘은 저번프로젝트때 진행했던 영화 게시판을 조금 다른 방식으로 만들어보았다.
- model form을 이용하여 사용자 요청 데이터의 유효성을 검증하고, http method또한 검사해보았다.
- 저번처럼 데이터를 생성, 조회, 수정, 삭제를 할 수 있는 Web application을 제작했는데, 조금만 방식을 바꾸었을 뿐인데 굉장히 배울 점이 많았다.





## 🧱 개발도구 및 라이브러리

1. Visual Studio Code
2. Google Chrome Browser
3. Bootstrap
4. Django 3.2.12 
   - pip install django==3.2.12



## 🔨 기본 틀 잡기

- 기본적으로 명세에 나와있는대로 틀을 잡았고, 바뀐점은 내가 TMDB API를 활용하여 제작하다보니, TMDB의 데이터에서 찾을 수 없었던 관람객 수(audience)를 빼고 흥행도(popularity)를 추가로 넣어 제작하였다.
- 흥행도는 Float 데이터 유형을 사용하였다.

- Model과  url은 pjt05와 거의 동일하였고, form설정이 조금 생소했다.
- 또한 new와 create 함수를 하나로 합쳤고, edit과 update함수를 하나로 합쳤다는 점이 조금 달랐다.
- form은 model과 같은 정보를 저장했고, 위젯을 이용하여 placeholder와 날짜의 경우 selectdatewidget을 활용했다. 





## 🌎 전체 영화 목록 조회(index.html)

![index](README.assets/index-16494275418191.PNG)

- 데이터 베이스에 존재하는 모든 영화들의 목록을 보여주는 페이지이다. 영화의 제목과 평점을 보여주며 제목을 클릭하면 해당 영화의 상세페이지로 넘어가게 만들었다.
- 상단에는 새로운 영화 데이터를 작성하는 페이지로 가는 [CREATE]라는 버튼도 만들었다.
- views의 index함수에서 **Movie의 모든 객체를 movies로 받아** 그 모든 데이터를 보여줄 수 있게 만들었다.
- 처음에 index페이지에 들어가면 api로 받아온 6개의 영화가 기본값으로 보여지고, new를 통해 새로운 데이터를 작성하면 추가적으로 보여진다.
- api로 영화를 받아올 때는 views.py에 **TMDB에서 제공하는 top_rated**의 영화정보 6개를 Movie객체로 만들어 저장해두었다.





## 🌈 영화 상세정보 페이지(detail.html)

![detail](README.assets/detail-16494276762622.PNG)

- 특정 영화의 상세 정보를 표시하는 페이지이다.

- index페이지에서 제목을 클릭했을 때, create페이지에서 새롭게 데이터를 작성하고 저장했을 때, update페이지에서 데이터를 수정했을 때 모두 각 영화의 detail페이지로 넘어오게 된다.

- 위 사진에서 보는 것과 같이 제목, 흥행도, 개봉일, 장르, 평점, 줄거리를 보여주며, 아래쪽에는 수정과 삭제, 그리고 index페이지로 넘어가는 back버튼을 만들어 주었다.

- detail페이지는 명세에 나와있는 것처럼 부트스트랩의 Card component를 사용해 주었다.

- 컴포넌트를 사용해서 그런지 사진 사이즈와 위치 조정말고는 쉽게 해결 가능한 페이지였다.

  



## 🌟 영화 작성 페이지(create.html)

![create](README.assets/create-16494278279203.PNG)

- 영화 정보를 작성하는 form을 표시하는 페이지 이다. submit을 클릭하면 detail페이지로 , back버튼을 누르면 index페이지로 이동한다.

- bootstrap5를 load받아 사용했기 때문데 사이즈 조정을 따로 안해줘도 꽤 보기 좋게 나왔다.

- 개봉일은 text나 float필드가 아니기 때문데 작성이 어려울 것 같아서 위젯을 사용하여 날짜를 선택할 수 있게 해주었다.

  ```python
  release_date = forms.DateField(
          input_formats=['%Y-%m-%d'],
          widget=forms.SelectDateWidget)
  ```

  

- 저번 프로젝트에서도  가장 고민했던 부분인 **genre**에서 오늘도 많이 헤맸다. 최대한 이전의 프로젝트를 많이 참조해서 연결되는 프로젝트를 만들려고 하는편인데, 저번에 views.py에서 genrelist를 받아 사용했던 방식으로는 이번에는 구현이 어려울 것 같았다. forms.py에서 리스트가 필요했는데, list타입의 변수를 views에서 import받으려고 한 생각이 잘 되지 않더라. 그래서 이번에는 forms.py에서 api를 한 번 더 불러와서 구현했다.

  ```python
  class MovieForm(forms.ModelForm):
      genrechoice = []
      for i in range(len(genrelist)):
          genrechoice.append((i, genrelist[i]))
      
      genre = forms.ChoiceField(
          choices = genrechoice,
          widget=forms.Select()
      )
  ```

- 클래스 전에 저번처럼 api로 genre만 불러왔고, 그 리스트를 class안에서 다시 선언했다. 그리고 select위젯을 사용하여 장르 데이터를 선택할 수 있도록 하였다.

- 처음에 create페이지를 만들었을때 submit이 안되고 같은 페이지를 계속 보여줬는데, 내가 create함수에서 if문으로 request.POST를 조건문으로 걸어야 하는데, request == 'POST'라고 조건문을 걸어놨었다. 얼핏 보면 같아보이지만 전혀 다른 동작이 되어 놀랐다.





## 🚀 영화 수정 페이지(update.html)

![update](README.assets/update-16494284667864.PNG)

- update페이지는 create페이지와 다른 점이 별로 없어서 수월하게 코드를 작성할 수 있었다. 

- 다른 부분은 update함수에서는 instance를 설정해주어야 한다는 점과, cancle버튼을 만들어서 초기화 할 수 있도록 만들어 주는 것이었다.

- cancle버튼은 a태그를 활용하였고,  url값을 주지 않아 버튼을 누르면 기존 값으로 돌아가게 해주었다.

  



## 💫 마무리

#### 오늘 내 실수들 + 배운 것들

- 앱을 만들기 전에 경로에 추가하면 안된다고 들었던 것 같은데, 오늘 한 번 bootstrap을 install받기전에 추가해서 오류가 났던 것 같다. installed app에는 무조건 앱을 만들거나 install받고 추가하자!
- 위에서도 언급했지만 if  request.POST와 if  request=='POST'는 다르다,,
- 몇 번을 했는데도 gitignore를 안만들고 add commit해서 자꾸 다시하게 된다,, ^^,,,
- 기존 방식이 안되면 빠르게 다른 방식을 찾아야 하는데 기존 방식에서 벗어나는 게 어렵다. 오늘도 genre때문에 한시간넘게 고민한 것 같은데 아닌 것 같으면 빠르게 다른 길을 찾아봐야겠다.
- 사실 오늘은 크게 어렵거나 복잡한 부분이 없었던 것 같다. 내가 명세를 잘 안읽고 내 멋대로 만든 걸 수도 있지만,.,ㅎㅎ 근데 프로젝트를 진행하다 보니 좀 더 예쁘게 꾸며보고 싶다는 생각을 자주 한다. 시간에 쫒겨서 호다닥 해야하는 프로젝트에서는 어렵겠지만, 따로 간단한 프로젝트라도 프론트까지 신경을 써서 마무리해보고 싶다!