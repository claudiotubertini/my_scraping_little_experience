# README
# Images are downloaded in the folder _immagini/ with nome _nome_
# In the main directory you will find the categories file in csv format, one for each category

library("rvest")
library("dplyr")
library("stringr")
library("httr")
library("XML")
library("curl")
set_config(config(ssl_verifypeer = 0L))

fun_example <- function() {
  pricetopf <- data_frame(minsan = character(),
                          title = character(),
                          price_scontato = character(),
                          price_listino = character(),
                          description = character() ,
                          description_short = character(),
                          image_url = character())
  catvec <- c("xxx", "yyyy", "zzzz")
  page_number <- 1
  for (j in catvec) {
    url <- paste0("https://www.example.com/", j, "/?n=36")
    firststart <- tryCatch(GET(url), warning = function(w){
      warning(w)
    }, error = function(e){
      "NA"
    }, finally = {"NA"})
    category = read_html(firststart)
    product_count <- category %>% html_node(".product-count") %>% html_text()
    m <- gregexpr("\\d+", product_count, perl=TRUE)
    product_count <- regmatches(product_count, m)[[1]][[3]]
    #product_count2 <- sub(".*?(\\d+)\\s.*", "\\1", product_count)
    page_number <- ceiling(as.numeric(product_count) / 36)

    for ( k in 1:page_number){
      #farmapage <- html(paste0(url, "&p=", k))
      secondstart <- tryCatch(GET(paste0(url, "&p=", k)),
                              warning = function(w){
                                warning(w)
                              }, error = function(e){
                                "NA"
                              }, finally = {"NA"})
      farmapage = read_html(secondstart)
      mylist <- tryCatch(farmapage %>% html_nodes("h5 a"), error = function(e){"NA"}, finally = {"NA"})
      names <- ifelse(mylist=="NA", "NA", mylist %>% html_attr("title"))
      link <- ifelse(mylist=="NA", "NA", mylist %>% html_attr("href"))

        for (i in 1:length(link)) {
          thirdstart <- tryCatch(GET(link[[i]]),
                                 warning = function(w){
                                   warning(w)
                                 }, error = function(e){
                                   "NA"
                                 }, finally = {"NA"})
          single_page <- tryCatch( read_html(thirdstart), error=function(e) e )
          if(inherits(single_page, "error")) next
          title <- tryCatch(names[[i]] %>% str_replace(",", "."), error=function(e){"NA"})
          minsan <- tryCatch(single_page %>%
                               html_node(".editable") %>%
                               html_text(), error = function(e){"NA"}, finally = {"NA"})
          price_scontato <- tryCatch(single_page %>%
                                       html_node("#our_price_display") %>%
                                       html_text() %>% str_extract("(\\d+,\\d+)") %>% str_replace(",", "."), error = function(e){"NA"}, finally = {"NA"})
          price_listino <- tryCatch(single_page %>% html_nodes("#old_price_display") %>%
                                      html_text() %>% str_extract("\\d+,\\d+") %>% str_replace(",", "."), error = function(e){"NA"}, finally = {"NA"})
          price_listino <- ifelse(length(price_listino)>0, price_listino, "NA")
          image_url <- tryCatch(single_page %>% html_node("#bigpic") %>% html_attr("src"), error = function(e){"NA"}, finally = {"NA"})
          image_name <- tryCatch(paste0(minsan,"_", tail(strsplit(image_url, "/")[[1]], n=1)),
                                 error = function(e){"NA.jpg"}, finally = {"NA.jpg"})
          html2 = thirdstart
          parsedhtml= tryCatch(htmlParse(html2, encoding="utf-8"), error = function(e) {"No connection"})
          if(inherits(parsedhtml, "error"))
          {description_html=""} else {description_html <- xpathSApply(parsedhtml, "//*[@id='idTab1']/div[2]/div[1]")} #//*[@id="idTab1"]/div[2]/div[1]

          description = paste(as.list(capture.output(description_html)[-1]), collapse = "")
          description <- ifelse(is.null(description), "Non disponibile", description)
          description_short <- tryCatch(single_page %>% html_nodes("#short_description_content") %>% html_text(), error = function(e){"Non disponibile"}, finally = {"Non disponibile"})
          description_short <- ifelse(is.null(description_short), "Non disponibile", description_short)
          pricetopf <- bind_rows(pricetopf, data_frame(minsan,
                                                       title,
                                                       price_scontato,
                                                       price_listino,
                                                       description,
                                                       description_short,
                                                       image_url))
        }

    }

    write.table(pricetopf, paste0("example_output_", j, ".csv"), na="", row.names = FALSE,
                quote=FALSE, sep="|", fileEncoding="UTF-8")
  }
}


fun_example()
