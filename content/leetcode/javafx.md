---
title: "Javafx开发总结"
date: 2022-07-03T12:04:04+08:00
tags: ["javafx"]
---











# javafx overview

这学期做的两个java项目（喵photoshop和喵wechat）中，我都承担了不少的javafx代码，现在磕磕绊绊也比较容易写出能跑的东西了。便介绍一下我对javafx的总结。

#### 官方介绍

 JavaFX 是一个开源的下一代客户端应用平台，适用于基于Java构建的桌面、移动端和嵌入式系统。 它是许多个人和公司的共同努力的成果，目的是为开发丰富的客户端应用提供一个现代、高效、功能齐全的工具包。

#### 项目结构
![请添加图片描述](https://img-blog.csdnimg.cn/bc383332321c4779a7e3d795b3719a07.png)



IDEA一路default后创建出来的javafx项目如图所示。

在src的package中，javafx程序的入口是Helloapplication，在其中调用了

```java
new FXMLLoader(HelloApplication.class.getResource("hello-view.fxml"));
```

是从对应的resourses中根据某个布局文件建立一个窗口，并通过一系列如`setTitle`, `setIcon`等方法进行配置，最后显示出来。

在`hello-view.fxml`中有

```java
fx:controller="com.example.demo1.HelloController"
```

意思是，这个布局文件绑定的控制类是`com.example.demo1.HelloController`。

综上所述，javafx项目的重要特点是，布局和功能分离，

综上所述，javafx项目的最基本结构就是，一个布局文件对应一个控制类（控制这个布局文件的某个按钮点击后调用什么方法等），然后从布局文件load一个窗口，进行愉快的交互。



#### 用SceneBuilder创建布局

![请添加图片描述](https://img-blog.csdnimg.cn/e6aa07657d5b48e5a46ff95d78ee758d.png)


javafx为创建布局提供了官方的很方便的工具：SceneBuilder，创建一个fxml文件以后右键用SceneBuilder点开，大约如图所示。
![请添加图片描述](https://img-blog.csdnimg.cn/4f8126b83050432e987a32a04e16fdf9.png)


我们可以在此拖拽各种部件到各种布局中，个人而言，HBox（里面的组件和子布局水平排列）和VBox（垂直排列）的嵌套可以解决绝大多数问题。

如上图所示布局，是在最外侧的`AnchorPane`布局中，放入一个VBox，VBox中放入三个HBox，每个HBox中间放置一个label和一个textfield，最下面的放置两个button，并对每一个布局设置其排列规律为水平垂直居中（如保证“帐号”标签和旁边的输入框在所在的HBox里水平垂直居中），再适当调整Margin（部件之间的距离），如设置“帐号”标签右边有20px的间隔，只需要这寥寥几布操作就可以做出这种基础又实用的布局文件。

在SceneBuilder中保存后的fxml文件实际如下：

![请添加图片描述](https://img-blog.csdnimg.cn/e0188cd1739c491b98b0651ad0baf8e4.png)

就像html一样用嵌套的标签和标签的属性确定出布局样式。还是可以拖拽的plus版，真神奇。



#### 为fxml添加样式

javafx可以使用css样式，前端狂喜。
![请添加图片描述](https://img-blog.csdnimg.cn/7ec7afbbee53458e964bc9a5a7c7cde4.png)


在SceneBuilder中选中组件就可以在右边添加样式，javafx的css阉割了不少，不过只要配色讲究一些也可以做的比较美观。

![请添加图片描述](https://img-blog.csdnimg.cn/7933a4de582f40c982a9fe3df1a80597.png)

如喵photoshop的最左边工具栏，实际上只是一个VBox中紧密排列着数个按钮，并对他们设置了取消圆角和背景颜色而已。（虽然看着很麻烦但是用拖拽很愉快的！）

```css
<Button id="button1" onAction="#choose" prefHeight="38.0" prefWidth="42.0" style="-fx-background-radius: 0;" textFill="WHITE">
      <graphic>
          <ImageView fitHeight="44.0" fitWidth="28.0" pickOnBounds="true" preserveRatio="true">
               <image>
                      <Image url="https://miaotu-headers.oss-cn-hangzhou.aliyuncs.com/photoshopicons/xuanze.png" />
               </image>
           </ImageView>
       </graphic>
</Button>
```

除了行内的css样式，我们同样可以引入css文件，上图中工具栏便引入了css文件。

不如说因为行内css不能写伪类选择器（`#button1:focused`代表被选中的button1），所以必须绑定一个css文件。

```xml
<VBox id="left" prefHeight="691.0" prefWidth="44.0" style="-fx-background-color: #424874;" stylesheets="@style.css">
    <Button id="button1"></Button>
    <Button id="button1"></Button>
    <Button id="button1"></Button>
</VBox>
```

```css
#button1 {
    -fx-background-color: #424874;
}

#button1:focused {
    -fx-background-color: #A6B1E1;
}
```

#### 控制类

上面提到，一个布局要绑定一个控制类，比如在喵wechat中，登录注册窗口要有一个单独的控制类，里面写着按下“登录”，“注册”按钮要做什么事；消息列表窗口有一个单独的控制器，里面写着怎么根据当前登录用户的不用而显示不同的用户头像，怎么获取这个用户的好友列表等，更不用谈消息窗口的“发消息”按钮如果没有绑定的控制类就更糟糕了。

我们接下来以最简单的编辑资料布局来谈控制类的用法。
![请添加图片描述](https://img-blog.csdnimg.cn/9a3669fc477f4cdf86ddfdd86b08974b.png)


```xml
<AnchorPane prefHeight="226.0" prefWidth="377.0" xmlns="http://javafx.com/javafx/18" xmlns:fx="http://javafx.com/fxml/1" fx:controller="com.mywechat.Edit">
   <children>
      <VBox alignment="CENTER" prefHeight="226.0" prefWidth="377.0">
         <children>
            <HBox alignment="CENTER" prefHeight="60.0" prefWidth="377.0">
               <children>
                  <Label text="个人简介" >
                  </Label>
                  <TextField fx:id="intro"/>
               </children>
            </HBox>
            <HBox alignment="CENTER" prefHeight="60.0" prefWidth="377.0">
               <children>
                  <Label text="头像url" >
                  </Label>
                  <TextField fx:id="url"/>
               </children>
            </HBox>
            <HBox alignment="CENTER" prefHeight="60.0" prefWidth="377.0">
               <children>
                  <Button mnemonicParsing="false" text="提交" onMouseClicked="#submit" />
               </children>
            </HBox>
         </children>
      </VBox>
   </children>
</AnchorPane>
```

从上面的布局文件的关键代码中可以看到，fxml的根节点标签中的

```java
fx:controller="com.mywechat.Edit"
```

便是为该布局文件绑定控制类的最关键代码。

布局和控制类的交互重点有两：

* 我们在fxml文件里给想要在控制类里引用的组件加一个`fx:id`属性，就可以在控制类里使用它。
* 给欲引起事件的按钮加上`onMouseClicked="#submit"`等，便代表点击后就可以调用控制类的submit方法。

要绑定事件的不只是按钮，可以是很多类型的组件，可以绑定的事件也不只是“鼠标点击”，也可以有“鼠标悬浮”，“鼠标拖拽”等等。

再看如下的控制类的代码，其功能一目了然。

```java
public class Edit {
	public Chatlistcont parentController=null;
	public TextField intro;
	public TextField url;
	public void initialize(){

	}
	public void setParentController(Chatlistcont parentController) {
		this.parentController = parentController;
	}

	public void submit(MouseEvent mouseEvent) {
		if(JdbcFirstDemo.updateuser(parentController.curname,intro.getText(),url.getText())==0){
			DialogPane dialog = new DialogPane();
			dialog.setHeaderText(" 恭喜！");
			dialog.setContentText(" 修改成功！");
			Stage dialogStage = new Stage();
			Scene dialogScene = new Scene(dialog);
			dialogStage.setScene(dialogScene);
			dialogStage.setResizable(false);
			dialogStage.show();
			parentController.intro.setText(intro.getText());
			parentController.avatar.setImage(new Image(url.getText()));
			parentController.update();
		}

	}
}
```



`public TextField intro; public TextField url;`是我们为之创建fx:id想要引用的组件，在提交方法中，我们通过`intro.getText()`, `url.getText()`获得其中的文字，再调用公共静态方法`JdbcFirstDemo.updateuser`提交到数据库中。

非常简单又优雅的操作对不对，布局和功能分离，真方便啊。



#### 创建窗口

一个javafx项目可能涉及不止一个窗口，如何建立窗口呢，可以先看看上面的Edit窗口是如何被创建出来的。

```java
	public void edit(MouseEvent mouseEvent) {
		Stage newStage = new Stage();//创建窗口，此时未显示
		FXMLLoader fxmlLoader = new FXMLLoader(HelloApplication.class.getResource("edit.fxml"));
        //获得布局文件的loader
		try {
			newStage.setScene(new Scene(fxmlLoader.load()));
            //通过loader生成一个scene，设置到窗口上
			Edit aa=fxmlLoader.getController();
			aa.setParentController(this);
			Users cur=JdbcFirstDemo.getuser(curname);
			aa.intro.setText(cur.intro);
			aa.url.setText(cur.avatar);
			newStage.setTitle("编辑资料");
            //对窗口进行标题，图标的设置
			newStage.getIcons().add(new Image("https://miaotu-headers.oss-cn-hangzhou.aliyuncs.com/javachat/avatar/tiantianquan.png"));
			newStage.show();
            //显示窗口
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
```

![请添加图片描述](https://img-blog.csdnimg.cn/99d2b1e24ebc416aba01a2d32b078277.png)


由此可见，javafx窗口的结构大概如图所示！

窗口就是窗口，场景存放布局，布局中就是我们在SceneBuilder中拖拽构建后生成的嵌套组织，那些我们所定义的`Label`, `Button`, `HBox`等，他们都继承于`Node`，也就是说他们都是各种不同类型的节点，嵌套组织于布局中。



#### 为布局动态添加子节点

我们会经常遇到为布局动态添加字节点的情况，比如：

![请添加图片描述](https://img-blog.csdnimg.cn/a32c932faf3f4fe39ee57f2defadcfc6.png)

![请添加图片描述](https://img-blog.csdnimg.cn/4d5f5423bfaf438fb91e6993c837b7b1.png)

如果有别的用户上线了，要添加到“当前在线”中，当我们选择关注或者取关某位用户，要动态地添加或者移除“我的关注”。

要操作的子节点我已经做成了布局文件`userinfo.fxml`

![请添加图片描述](https://img-blog.csdnimg.cn/5723e77772584fc89290696acb116f21.png)


这里我经常是这么处理的，请看关键代码

```java
public VBox all;//是当前在线列表的容器
public void update(){
		all.getChildren().clear();//先清空容器
		int len=ret.size();//ret是服务器返回的用户列表
		for(int i=0;i<len;i++)
		{
			FXMLLoader loader = new FXMLLoader(HelloApplication.class.getResource("userinfo.fxml"));
			AnchorPane tmp=null;//userinfo.fxml的根节点是AnchorPane
			try {
				tmp=(AnchorPane) loader.load();
			} catch (IOException e) {
				e.printStackTrace();
			}
			all.getChildren().add(tmp);
		}
	}
```

`getChildren()`方法可以获得节点的子节点列表，可以`clear()`或者`add()`。通过这种方法可以动态改变布局。

#### 布局load()可以获得控制类实例

这是笨蛋的我宝贵的摸索出的经验！

![请添加图片描述](https://img-blog.csdnimg.cn/21e62a070b624104a024380e4826d9e8.png)


在开发photoshop的时候，我希望点击外部的容器的“+”就可以通过`getChildren().add()`在列表中加上一个从fxml文件加载的子节点（就像上面一样），但是我希望在每个子结点上放一个“-”按钮，点击后可以删除这个图层。

但是若要在布局中删除这个子节点的话，必然不能让这个子节点的控制类自己删除自己，只能先获得它爹，再调用他爹的`getChildren.remove()`，但是`getChildren`不是公有方法，我一度以为不能通过点击子结点上的删除按钮删除自己，所以在父结点上做了删除按钮，选中要删除的子节点后点击父结点上的按钮再删除。

后来我才知道，javafx有一个很重要的实质，也就是load一次布局就相当于创建了一个控制类实例，如下：

![请添加图片描述](https://img-blog.csdnimg.cn/46265932ecc34761834ce792b0932690.png)


如果我们点击了子节点item上的删除按钮的时候可以获得container的控制类实例，就可以调用父节点删除子节点自己了。

返回那个在线聊天室的例子。

不难看出，聊天室的上面的代码只能达成有几个在线用户就加几个默认样式的`userinfo.fxml`的效果，上面的用户头像或者名字不会随着变化，

真正的关键代码应该是如下的：

```java
public VBox all;//是当前在线列表的容器
public void update(){
		all.getChildren().clear();
		int len=ret.size();
		for(int i=0;i<len;i++)
		{
			FXMLLoader loader = new FXMLLoader(HelloApplication.class.getResource("userinfo.fxml"));
			AnchorPane tmp=null;
			try {
				tmp=(AnchorPane) loader.load();
			} catch (IOException e) {
				e.printStackTrace();
			}
			Userinfo aa=loader.getController();//获得了子节点的控制类实例！
            //Userinfo是因为fx:controller="com.mywechat.Userinfo"
			aa.setParentController(this);//
			aa.from=curname;
			aa.socket=this.socket;
			aa.name.setText(ret.get(i).name);
            //在父结点中操作子节点很方便！
            //这样就可以改子节点的名字了
			aa.intro.setText(ret.get(i).intro);
            //这样就可以改子节点的自我介绍了
			aa.avatar.setImage(new Image(ret.get(i).avatar));
            //这样就可以改子节点的头像了
			aa.online=true;
			int len1=retstar.size();
			all.getChildren().add(tmp);
		}
	}
```



```java
public class Userinfo {
	public String from;
	public Label name;
	public Label intro;
	public ImageView avatar;
	private Chatlistcont parentController;//他爹
    
	public void setParentController(Chatlistcont parentController) {
		this.parentController = parentController;
	}
    
    ...
        
    public void gotostar()//按下关注按钮以后，父节点代表的当前登录用户，关注这个子节点代表的用户
	{
		JdbcFirstDemo.staruser(from,name.getText());
        //在子结点中调用父节点的方法也很方便了！
		parentController.updatestar();
        //新关注一个人以后，父容器update一下，刷新UI
		parentController.update();
	}
}
```

一旦掌握了这种在load布局时，就建立控制类实例之间的关系的方法的话。整个javafx项目中的各个节点都可以根据需要像蜘蛛网一样连接在一起，互相调用方法，获得变量都非常非常方便，开发难度会骤减。



#### 手敲代码建立布局

在实际开发中，并不是所有时候都更适合load布局文件来组织布局的。

比如喵photoshop的下面的情况，每选一个不同的工具，下方的工具栏就会显示不同的组件，难道要为十几个工具都建一个fxml专门放在下面吗？显然有点小题大做了。



![请添加图片描述](https://img-blog.csdnimg.cn/108a067eda6f4b2b8e8a51e8693e1cc7.png)
![请添加图片描述](https://img-blog.csdnimg.cn/06e842dcb2e54cd2b0ed4fa1b2d9859b.png)


```java
public HBox down;//下面一长条
public void pen() {//点击钢笔工具以后
		down.getChildren().clear();
    
		Label label1=new Label("钢笔工具");
		label1.setPadding(new Insets(4,5,0,5));
    	label1.setTextFill(Color.WHITE);
    
		Label label2=new Label("选择粗细(px)");
		label2.setPadding(new Insets(4,5,0,5));
		label2.setTextFill(Color.WHITE);
    
    
        ColorPicker colorPicker=new ColorPicker();

   		TextArea gangbicuxi=new TextArea();
		gangbicuxi.setMaxWidth(30);
    
		Button enter=new Button("确定");
		enter.setOnAction(
				event -> {
				//点击按钮的事件
				}
		);
		
    	
    down.getChildren().addAll(label1,colorPicker,label2,gangbicuxi,enter);
}
```

我是这么处理的，直接在方法中也可以定义组件，设置组件的属性，然后

```java
down.getChildren().addAll(label1,colorPicker,label2,gangbicuxi,enter);
```

就可以让下面的长条变成这样。

![请添加图片描述](https://img-blog.csdnimg.cn/47e32cd03e10410dacf43adac56e3a0c.png)




fxml加载布局和代码手撸布局基本是可以互相转换的，可以做到彼此可以做到的事情。不过平常用SceneBuilder非常方便罢了。



#### java+mysql

虽说和javafx没有什么关系，不过这是我第一次在别的语言中用数据库，我觉得非常神奇。

**增**

```java
public static int adduser(String name1,String password1) {

		try{
			//1. 加载驱动
			Class.forName("com.mysql.cj.jdbc.Driver");//固定写法
			//2. 用户信息和url
			//useUnicode=true&characterEncoding=utf8&&useSSL=true
			String url="jdbc:mysql://xxxxxxxxxxxxxx.mysql.rds.aliyuncs.com:3306/mywechat?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=GMT%2B8";
			String name = "root";
			String password = "xxxxxxx";

			//3. 连接成功，返回数据库对象  connection代表数据库
			Connection connection= DriverManager.getConnection(url,name,password);
			//4. 执行SQL的对象 statement 执行SQL的对象
			Statement statement = connection.createStatement();

			//5. 执行SQL的对象 去执行SQL  
			String sql="insert into userinfo(username, password) values ('"+name1+"','"+password1+"');";
			System.out.println(sql);
			statement.execute(sql);

			//6. 释放连接

			statement.close();
			connection.close();
			return 0;

		}
		catch (Exception e)
		{
			e.printStackTrace();
			return 1;
		}

	}
```



**删**

```java
			Statement statement = connection.createStatement();
			String sql="delete from userstar where username1='"+name1+"' and username2='"+name2+"';";
			statement.execute(sql);
```



**查**

```java
			Connection connection= DriverManager.getConnection(url,name,password);
			//4. 执行SQL的对象 statement 执行SQL的对象
			Statement statement = connection.createStatement();
			ArrayList<Users> tmp=new ArrayList<>();
			//5. 执行SQL的对象 去执行SQL   可能存在结果，查看返回结果
			String sql="SELECT * FROM userstar WHERE username1='"+name1+"'";
			//System.out.println(sql);
			ResultSet resultSet = statement.executeQuery(sql);//返回的结果集,结果集中封装了我们全部查询的结果
			while(resultSet.next()){
				String starring=resultSet.getObject("username2").toString();
				Users ret=getuser(starring);
				tmp.add(ret);
			}
			//6. 释放连接
			resultSet.close();
			statement.close();
			connection.close();
```



对于增删改这种不需要返回一条条记录的操作，我们只需要这样，返回一个boolean

```java
statement.execute(sql);
```

对查询操作，需要不同的语句，返回一个结果集

```java
ResultSet resultSet = statement.executeQuery(sql);//返回的结果集,结果集中封装了我们全部查询的结果
while(resultSet.next()){
	String starring=resultSet.getObject("username2").toString();
	//balabala
	}
//释放连接
resultSet.close();
```

操作数据库比想象的比简单很多，非常方便！



#### 结语

这是我两次贫瘠的javafx开发经验为我带来的一些学习总结，我实在觉得javafx开发起一些小东西很优雅，因为wpf太强大了我学不会，qt也觉得好麻烦......

我开发javafx项目的总时间共不到两天：

大作业答辩前一天晚上通宵从零写到第二天下午答辩喵photoshop；

昨晚从零通宵到现在开发喵wechat。

可以独立开发小的桌面应用的感觉很不错！
