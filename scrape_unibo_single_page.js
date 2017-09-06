

var webPage = require('webpage');
var page = webPage.create();
var system = require('system');
var args = system.args;
var fs = require('fs');
var path = 'myunibo_single_page.html';

var url_base = 'http://www.unibo.it/UniboWeb/UniboSearch/Rubrica.aspx?tab=PersonePanel&mode=advanced&lang=it&query=%2binizialecognome%3a';
var mypage = url_base + args[1] + '&page=' + args[2];
page.open((mypage), function (status) {
  var content = page.content;
  fs.write(path,content,'w');
  phantom.exit();
});