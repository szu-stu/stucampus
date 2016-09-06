function introduce(bm){
	var intro = document.getElementById("intro");
	a = document.getElementById("cb");
	b = document.getElementById("js");
	c = document.getElementById("xz");
	d = document.getElementById("sj");
	e = document.getElementById("yy");
	if(bm==1){
		$(a).removeClass("act");
		$(b).addClass("act");
		$(c).addClass("act");
		$(d).addClass("act");
		$(e).addClass("act");
		intro.innerHTML = "<h3>采编部</h3><h1>作为校级媒体报道校园活动、采访校内精英人物、采写优秀图文作品， 在此基础上负责新闻通知、深大摄影、人物专访等网站版块的制作与更新。加入采编，优先参与各种高大上的校级活动，优先与深大传奇人物近距离接触，在实践与思考中体会青春百味！</h1>" ;
	}
	else if(bm==2){
		$(a).addClass("act");
		$(b).removeClass("act");
		$(c).addClass("act");
		$(d).addClass("act");
		$(e).addClass("act");
		intro.innerHTML = "<h3>技术部</h3><h1>若是生于大航海时代，我们就会毫不犹豫选择出海。今互联网之时代，我们便敲起了键盘。代码如诗，我们为读到漂亮的程序而兴奋；文档如山，我们为辟出完美的路径而探索。我们编写网站，我们开发App，我们维护服务器，我们是学子天地技术部。</h1>";
	}
	else if(bm==3){
		$(a).addClass("act");
		$(b).addClass("act");
		$(c).removeClass("act");
		$(d).addClass("act");
		$(e).addClass("act");
		intro.innerHTML = "<h3>行政部</h3><h1>行政部如同学子天地的大脑，负责办公室事务，主要进行会议策划组织，落实组织内部制度执行情况，以严肃活动的态度保证学子天地的常态化、系统化和科学化的运作。这支高度规范化的队伍正在招新。</h1>";
	}
	else if(bm==4){
		$(a).addClass("act");
		$(b).addClass("act");
		$(c).addClass("act");
		$(d).removeClass("act");
		$(e).addClass("act");
		intro.innerHTML = "<h3>设计部</h3><h1>设计部从事网站页面和周边产品的设计，在掌握各类设计工具如PS、AI的基础上，运用平面设计和网页设计的相关技术、为用户呈现最佳的视觉体验。我们从一切事物与情绪中疯狂汲取灵感，我们在死线面前对全部细节与原则仍着魔般地坚持。我们相信这份坚持和执着能吸引有着相同信念的人加入，和我们并肩作战。</h1>";
	}
	else if(bm==5){
		$(a).addClass("act");
		$(b).addClass("act");
		$(c).addClass("act");
		$(d).addClass("act");
		$(e).removeClass("act");
		intro.innerHTML = "<h3>运营部</h3><h1>运营部作为学子天地里比较年轻的部门，肩负着大胆创新，突破自我的重任。目前的工作重点放在新媒体的运营上，不仅针对每一个新功能实现进行微信、微博上的推送宣传，还会进行站点的数据分析进而开始后续新功能的策划开发。欢迎每一个有想法、有能力的你的加入我们。</h1>";
	}
}