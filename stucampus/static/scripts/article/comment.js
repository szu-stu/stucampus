var StuComment = {
  comments: [],
  commentCount: 0,
  pk: parseInt(window.location.href.split('/')[4]),
  createNode: function() {
    //the methods to create a comment cards
    var elementType = arguments[0]
    var elementClass = arguments[1]
    var elementText = arguments[2]
    var dom = document.createElement(elementType)
    dom.className += elementClass
    if ((typeof elementText) != 'undefined') {
      var domText = document.createTextNode(elementText)
      dom.appendChild(domText)
    }
    return dom
  },
  getData: function() {
    //the methods to get all comment
    $.ajax({
      url: 'http://stu.szu.edu.cn/comment/get',
      data: {
        pk: this.pk
      },
      success: result => {
        this.comments = result.comment
        this.commentCount = result.commentCount
      }
    })
  },
  createComment: function() {
    //the way to create comment
    var item = arguments[0]
    var comments = this.createNode('div', 'comments')
    var userInfo = this.createNode('div', 'user_info')
    var avatar = this.createNode('img', 'avatar')
    var profindex = Math.round(Math.random()*3)
    avatar.src += '/static/images/articles/avatar' + profindex + '.jpg'
    var name = this.createNode('p', 'name', item.userName)
    var data = this.createNode('p', 'c_createtime', item.createTime)
    var delbtn = this.createNode('a', 'deletebtn', '删除')
    var message = this.createNode('span', 'message', item.commentContent)
    userInfo.appendChild(avatar)
    userInfo.appendChild(name)
    userInfo.appendChild(data)
    userInfo.appendChild(delbtn)
    comments.appendChild(userInfo)
    comments.appendChild(message)
    var f = document.getElementsByClassName('ds-thread')[0]
    f.appendChild(comments)
  },
  ready: function() {
    //the function while the page onload
    var _this = this
    this.getData()
    setTimeout(function() {
      if(_this.comments) {
        _this.comments.forEach(function (item) {
          //deal the objects to create a dom element
          _this.createComment(item)
        })
      }
    }, 1000)
  },
  post: function() {
    //the function to post the comment
    var content = $('.addcomment').val()
    //maybe we should detect the code for it can post right
    //所以开始用ajax了
    $.ajax({
      url: 'http://stu.szu.edu.cn/comment/add',
      data: {
        commentContent: content,
        articleId: this.pk
      },
      type: 'POST',
      success: res => {
        //返回一条json以作更新评论的玩意
        this.createComment(res)
        $('.addcomment').val("")
        StuCampus.notice('提交成功', 2000)
      },
      error: res => {
        StuCampus.notice('发生不可预料的错误', 2000)
      }
    })
  },
  delete: function() {
    //a methods to del aim comment
  }
}


setTimeout(function() {
  StuComment.ready()
  $('.submit').click(function() {
    StuComment.post()
  })
}, 3000)
