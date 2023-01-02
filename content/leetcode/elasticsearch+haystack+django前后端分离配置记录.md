---
title: " elasticsearch+haystack+django前后端分离配置记录"
date: 2023-01-03T00:04:04+08:00
tags: ["django"]

---

## elasticsearch+haystack+django前后端分离配置记录

这次的大作业需要做一个类似于知网的学术网站。（数据量是几亿数量级的）（也就是要做大量的全文检索）（这么大的数据，要是直接用sql语句select \* from article where abstract like '%linux%';要花很久很久）（这是根据mysql底层的数据索引方式决定的）（反正就是要花很久）（但是es进行这种全文检索就比较快，应该是毫秒级别的）（所以只能用es检索）（但是es和mysql存在的价值各有侧重）（es虽然也能算是一种数据库，但是只擅长检索，没有什么好的备份恢复机制，增删改也不太行）（所以我们的方案是在mysql里存，然后通过监听mysql加一条，es也加一条，查的时候在es里面查）（又因为我们用的是django后端框架，有一个有点好用但是又不太好用的东西叫haystack，提供了django里对es的一系列api），各种技术栈都比较陌生，也比较折磨，所以写个博客纪念。

首先，本教程的前半部分（配置部分）是参考的：https://blog.csdn.net/qq_52385631/article/details/126590931。可以直接照着它做，做完了来这里补充后半部分。



### 1.安装elasticsearch

按理来说elasticsearch的最新版本是8.5，但是haystack框架（Haystack是 Django 框架的搜索扩展模块）最高只支持es7.x，所以我选择安装elasticsearch7.17

方式详见：https://www.elastic.co/guide/en/elasticsearch/reference/7.17/targz.html

```shell
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.17.8-linux-x86_64.tar.gz
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.17.8-linux-x86_64.tar.gz.sha512
shasum -a 512 -c elasticsearch-7.17.8-linux-x86_64.tar.gz.sha512 
tar -xzf elasticsearch-7.17.8-linux-x86_64.tar.gz
cd elasticsearch-7.17.8/ 
```

es不支持root用户运行，所以需要为此新建一个es:es用户，切换到该用户下，运行`./bin/elasticsearch`。访问http://localhost:9200/，如果能看到类似这样的json：

```json
{
  "name" : "Cp8oag6",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "AT69_T_DTp-1qgIJlatQqA",
  "version" : {
    "number" : "7.17.8",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "f27399d",
    "build_date" : "2016-03-30T09:51:41.449Z",
    "build_snapshot" : false,
    "lucene_version" : "8.11.1",
    "minimum_wire_compatibility_version" : "1.2.3",
    "minimum_index_compatibility_version" : "1.2.3"
  },
  "tagline" : "You Know, for Search"
}
```

就算成功了。

迄今为止的es只能通过类似sql语句一样的命令（比如`GET /`）来访问数据。为了有一个像datagrip一样的可视化界面可以直接用鼠标点点增删改查，我安装了es官方的可视化工具（kibana）。

方式详见：https://www.elastic.co/guide/en/kibana/7.17/targz.html



### 2.配置django

官方文档：https://django-haystack.readthedocs.io/en/master/tutorial.html

```
pip install django-haystack
```

```json
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',

    # Added.
    'haystack',

    # Then your usual apps...
    'blog',
]

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch7_backend.Elasticsearch7SearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}


# 自动更新索引(即，用python语句操作model的时候能同步到es中，但是直接操作mysql就不会同步到es中，只能重建索引来同步)
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
# 设置每页显示的数目，默认为20，可以自己修改
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 8
```





**建立app和model**

```python
from django.db import models
 
 
class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=225)
 
    def __str__(self):
        return self.username
 
 
class Tag(models.Model):
    name = models.CharField(verbose_name='标签名称', max_length=225)
 
    def __str__(self):
        return self.name
 
 
class Article(models.Model):
    title = models.CharField(verbose_name='标题', max_length=225)
    content = models.CharField(verbose_name='内容', max_length=225)
    username = models.ForeignKey(verbose_name='用户', to='UserInfo', on_delete=models.DO_NOTHING)
    tag = models.ForeignKey(verbose_name='标签', to='Tag', on_delete=models.DO_NOTHING)
 
    def __str__(self):
        return self.title
```



**为表模型创建索引，search_indexes.py**

如果你想针对某个app，例如blog做全文检索，则必须在blog的目录下面，建立search_indexes.py文件，文件名不能修改，必须叫search_indexes.py

![88b8fa1df77d438eac3209fc0ea816f6](https://miaotu-headers.oss-cn-hangzhou.aliyuncs.com/typora/88b8fa1df77d438eac3209fc0ea816f6.png)

```python
from haystack import indexes
from .models import Article
 
 
# ArticleIndex：固定写法 表名+Index
class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    # 固定写法  document=True：haystack和搜索引擎，将给text字段分词,建立索引,使用此字段的内容作为索引进行检索
    # use_template=True,使用自己的模板,与document=True进行搭配，自定义检索字段模板(允许谁可以被全文检索,就是谁被建立索引)
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr='content')
    username = indexes.CharField(model_attr='username')
    tag = indexes.CharField(model_attr='tag')
 
    def get_model(self):
        # 需要建立索引的模型
        return Article
 
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        # 写入引擎的数据,必须返回queryset类型
        return self.get_model().objects.all()
```



可以粗浅地认为，上面的类的那些成员变量，一定要有一个是document=True, use_template=True的，并且这个的字段一定要叫text（可以在settings.py里面改全局变量从而设成别的，详见haystack官方文档，但是没有必要）

下面那些就是你希望可以拿来检索的其他字段。（也可以只有text但是必须有text）

![ea7ee1e2bba14619bd26d6af0f09f425](https://miaotu-headers.oss-cn-hangzhou.aliyuncs.com/typora/ea7ee1e2bba14619bd26d6af0f09f425.png)

```
{{ object.title }}
{{ object.content }}
{{ object.username.username }}
```

怎么解释上面的这个文件呢。



在model中，我们定义：

```python
class Article(models.Model):
    title = models.CharField(verbose_name='标题', max_length=225)
    content = models.CharField(verbose_name='内容', max_length=225)
    username = models.ForeignKey(verbose_name='用户', to='UserInfo', on_delete=models.DO_NOTHING)
    tag = models.ForeignKey(verbose_name='标签', to='Tag', on_delete=models.DO_NOTHING)
```

也就是说在我们的mysql中，article这个表我们定义了四个字段，分别叫title，content，username，tag。

上面我们的ArticleIndex类里面提到：

```python
text = indexes.CharField(document=True, use_template=True)
title = indexes.CharField(model_attr='title')
content = indexes.CharField(model_attr='content')
username = indexes.CharField(model_attr='username')
tag = indexes.CharField(model_attr='tag')
```

也就是说，在es中，我们定义了五个字段，其中title字段和mysql的title字段一样，content字段和mysql的content字段一样......text字段是一个高度自定义的字段，也是es底层的索引参考的字段（也就是按着搜索text字段效率最高的方式建立的索引）。text具体是什么呢，就是artice_text.txt的内容。

加入文件内容是

```
{{ object.title }}
{{ object.content }}
{{ object.username.username }}
```

如果这一条记录的title叫三国演义，content叫桃园三结义，他的username外键的username叫罗贯中，那这条记录的text字段就是

```
三国演义
桃园三结义
罗贯中
```



迄今为止，我们的es的索引就配置好了。我们所建立的es的表名叫做“haystack”（在settings.py里面定的），这个表里面包含article类的记录。如果我们在mysql数据库的article表里添加一些数据，然后运行`python manage.py rebuild_index`（这叫重建索引），就可以把mysql的article表的数据按照我们定义的规则添加到es的haystack表里面。

### 3.配置前后端分离检索api

这里有两个haystack里面的重要概念。一个是view一个是form。具体他们是什么，我也没有很精确地搞懂。但是我勉强可以理解他们是怎么使用的。

在我的理解下，一组form+view代表了一种搜索行为。

在一个app下的forms.py中定义form，在search_views中定义view。

在urls.py中，加上一个路由。这代表访问该路由就可以使用MyScholarSeachView+ScholarkeywordSearch提供的一种搜索行为。

```python

from scholar_data import search_views
from scholar_data import forms


urlpatterns = [
    path('api/search/scholarsearch/', search_views.MyScholarSeachView(
        form_class=forms.ScholarkeywordSearch
    ), name='haystack_search'),
]
```

其中的第二个参数就是你为某种搜索行为定义的一个haystack.views.SearchView的子类的实例，其构造的参数form_class代表了这个view要和哪个form绑定。

当一个SearchView接收到一个前端的get检索请求，把这个请求丢给他的searchform，让searchform的search函数进行搜索，返回结果集合，然后SearchView对这个结果集合进行封装，返回一个httpresponse。



haystack把一切搜索行为都理解成了填写一个form提交表单根据表单检索。你通过前端api送来的检索请求，在haystack看来就是填了个表单发过来，获取到的是一个form类的实例。form类在search方法里通过解析这个form，得到每一个空填的都是什么，然后进行检索，得到最终结果集，传给view。

view里面有一个方法叫做create_response，这是一个负责接受检索结果集，把它封装成httpresponse传给前端的方法。

```javascript
axios.get('http://120.46.153.189/api/search/scholarsearch',
            {
              params:{'q': 123,
                      'searchtitle':'meow',
                      'searchauthor':'xf',
                      'sorttype':1,
                      'begindate':1950,
                      'enddate':2000
                     }
            }).then((res)=>{
              console.log(res.data.data)
        })
```



```python
from django import forms
from haystack.forms import SearchForm
import json
from .models import Papers
from haystack.query import SQ,SearchQuerySet
class ScholarkeywordSearch(SearchForm):
    sorttype = forms.CharField(required=False)
    searchtitle = forms.CharField(required=False)
    searchauthor = forms.CharField(required=False)
    begindate = forms.CharField(required=False)
    enddate = forms.CharField(required=False)
    # 想当于建立了一个表单，这个表单固定有一个q，有我们自定义的sorttype，searchtitle，searchauthor，begindate，enddate( 如果没有前端发来的请求没有q就是不合法的，具体可以读源码)
    def search(self):
        type1=self.cleaned_data['sorttype']
        # 按理来说获取前端请求参数应该是paperID = request.POST.get('paperID')
        # 但是在form里就要把请求当作是一个表单，获取表单内容
        searchtitle1=self.cleaned_data['searchtitle']
        searchauthor1=self.cleaned_data['searchauthor']
        date1=self.cleaned_data['begindate']
        date2=self.cleaned_data['enddate']
        # 迄今为止 我们已经获取到了前端的请求里面的“sorttype”，“searchtitle”等参数。要根据这个写检索语句。
        sqs = SearchQuerySet().filter(SQ(title=searchtitle1) & SQ(author=searchauthor1)).filter(year__gte=date1).filter(year__lte=date2)
        if(type1==1):
            sqs = sqs.order_by('-n_citation')
        elif(type1==2):
            sqs = sqs.order_by('-n_citation')
        elif(type1==3):
            sqs = sqs.order_by('-year')
        elif(type1==4):
            sqs = sqs.order_by('year')
		# 还可以加排序，-代表倒序。默认按相关度排的。也就是type1==0的时候不刻意加orderby就是按相关度排序的结果
        sqs=sqs.load_all().highlight()
        print("查询到"+str(sqs.count())+"个结果")
    
        return sqs
```

简而言之，form的作用就是把http请求当作一个表单来解析，用一系列检索语句，搞种种带逻辑运算的filter和order_by。把结果集返回。

其中关于检索语句的部分，可以参考官方文档。

https://django-haystack.readthedocs.io/en/master/searchqueryset_api.html

https://django-haystack.readthedocs.io/en/master/searchquery_api.html

比如 哪个字段包含什么，哪个字段大于什么小于什么。都有特定的filter语句。甚至对哪个字段提高相关权重多少多少也都可以做到。



```python
from haystack.views import SearchView
from .models import *
from django.http import JsonResponse


class MySeachView(SearchView):

    def create_response(self):
        print(self.request)
        context = self.get_context()
        # 可以从这里获取到form的search函数返回的结果集
        data_list=[]
        for i in context['page'].object_list:
            # 这里也比较抽象，page应该是前端的get请求传过来的一个参数，但是没有的话默认就是0。代表返回搜索结果第page页的结果。（一页能有多少结果在settings.py里设置了。haystack原则上不支持把所有检索结果都返回，只支持返回第几页的结果。）
            data_dict={}
            data_dict['title']=i.object.title
            data_dict['topic']=i.object.topic
            data_dict['content']=i.object.content
            data_dict['auth']=i.object.auth
            data_dict['asso']=i.object.asso
            data_dict['jour']=i.object.jour
            data_dict['date']=i.object.date
            data_list.append(data_dict)
        print(len(data_list))
        print(data_list)
        return JsonResponse(data_list,safe=False)
```

searchview的作用就是把sqs结果集合分页再封装封装成http response返回给前端。



我曾经想过，urls.py里官方例程上的检索api都长得很特殊。能不能让它像其他注册登录的api一样，都定位到某个app的views.py的某个函数，在读过源码以后我觉得这应该是可以实现的，虽然还没有试验过。

```python
@csrf_exempt
def search(request):
    if request.method == 'GET':
        sv=MySearchView(form_class=forms.keywordSearch)
        return sv(request)
```



haystack的源码的类和类的属性和方法错综复杂，经常有比如这个类的这个方法的返回值就是那个类的那个方法的返回值这样抽象的情况。在我摸索出来的套路中，我只用到了form的search方法和searchview的create_response方法，但是实际上每个类都应该能有个几十种方法。我只是在完全不懂的情况下摸索出了一套能跑通的套路而已。



haystack虽然有一份官方文档，但是其他资料也很少，而且官方文档和绝大部分资料都是应对的前后端不分离的情况（为什么form把http请求当成form来解析，就是因为haystack本身就是为了直接和django的html模板对接而设计的），所以需要多读文档，多读源码，才能应对多种多样抽象的情况。



此外，我们还遇到了mysql和es的迁移的问题（默认安装在系统盘，要迁移到数据盘）es的迁移比较简单，直接改一个配置文件就可以，网上都可以搜到，mysql的迁移比较抽象，曾经给我带来了巨大的困扰，还好最后解决了。

![IQ}8E@3M}SWM`RB$K%7`K35](https://miaotu-headers.oss-cn-hangzhou.aliyuncs.com/typora/IQ}8E@3M}SWM`RB$K%7`K35.png)
