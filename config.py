import configparser

config = configparser.ConfigParser()


url={
    "search":"https://www.google.com/search?hl={}&q={}&q={}&num=5&ie=UTF-8",
    "search_bing":"http://www.bing.com/search?q={}+{}+{}&num=15",
    "search_duckgo":"https://www.duckduckgo.com/html?q={}+{}+{}&t=66hm&va=q",
    "headers":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15",
    "working_directory":"D:/PROJECT/Rest-api/Content-Categorization/skb/"
}
solr={
    "url":"http://52.53.165.238:8983/solr"
}


