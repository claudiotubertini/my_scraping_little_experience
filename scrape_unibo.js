

var webPage = require('webpage');
var page = webPage.create();

var fs = require('fs');
var path = 'myunibo.html'

page.open('http://www.unibo.it/UniboWeb/UniboSearch/Rubrica.aspx?tab=PersonePanel&mode=advanced&lang=it&query=%2binizialecognome%3aA', function (status) {
  var content = page.content;
  fs.write(path,content,'w')
  phantom.exit();
});