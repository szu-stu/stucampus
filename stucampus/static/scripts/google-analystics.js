//google流量统计
  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-19280508-1']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = '/static/scripts/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
    try{
        _ga._addOrganic("baidu","word");
        _ga._addOrganic("soso","w");
        _ga._addOrganic("yodao","q");
        _ga._addOrganic("sogou","query");
        _ga._addOrganic("6sou.szu.edu.cn","query");
      }catch(err){}
  })();
