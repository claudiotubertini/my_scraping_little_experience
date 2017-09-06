library(stringr)
library(rvest)
library(dplyr)
library(XML)
library(tidyr)

df <- as.data.frame(t(rep("",8)), stringsAsFactors = FALSE)
catlet = c('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
#vector_names = c('nome', 'ruolo','struttura', 'indirizzo','email', 'tel', 'fax', 'web', 'vcard')
#url = "http://www.unibo.it/UniboWeb/UniboSearch/Rubrica.aspx?tab=PersonePanel&mode=advanced&lang=it&query=%2binizialecognome%3a"

for (j in catlet) {
  system(paste("phantomjs", "scrape_unibo_single_page.js", j, 1, sep = " "))
  category <- read_html('myunibo_single_page.html')
  product_count <- category %>% html_node("#PersoneResults_RisultatiRicerca") %>% html_text()
  product_count =  str_extract(product_count, "(\\d+).*?")
  page_number <- ceiling(as.numeric(product_count) / 15)



  data_sequence <- category %>% html_nodes(xpath = "/html/body/div/div[2]/div[4]/table")
  records = lapply(data_sequence, html_table)
  for (i in 1:15){
    drec = t(records[[i]]['X2'])
    df <- bind_rows(df, as.data.frame(drec))
  }
  # retrieve data from the following pages
  # http://www.unibo.it/UniboWeb/UniboSearch/Rubrica.aspx?tab=PersonePanel&mode=advanced&lang=it&query=%2binizialecognome%3aA&page=2
  for(k in 2:page_number){
    system(paste("phantomjs", "scrape_unibo_single_page.js", j, k, sep = " "))
    single_page = read_html("myunibo_single_page.html")
    data_sequence <- single_page %>% html_nodes(xpath = "/html/body/div/div[2]/div[4]/table")
    records = lapply(data_sequence, html_table)
    for (i in 1:length(records)){
      drec = t(records[[i]]['X2'])
      df <- bind_rows(df, as.data.frame(drec))
    }
  }
}
df$V6 = str_trim(sub("\\s+", " ", df$V6))
df$V6 = stri_replace_all_charclass(df$V6, "\\p{WHITE_SPACE}", " ", merge=TRUE)

write.table(df, "unibo4.csv", na="Non presente", sep=";", fileEncoding = "UTF-8")