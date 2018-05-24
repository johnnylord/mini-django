# mini-django
## Handlers

## Middleware
Middleware是一個在request和response processing中會先進行預處理的區塊
每個middleware都需要繼承MiddlewareMixin這個class,並且根據需求實做process_request()和process_response(),並且要將會使用到的middleware路徑寫在settings.py中MIDDLEWARE的List裡面
#### process_request()
在request被使用者所定義function處理前,需要對request進行預處理時,需要實做process_request()
#### process_response()
在response被送回使用者之前,需要對response進行預處理時,需要實做process_response()
### load_middleware
![](https://i.imgur.com/IUTKd1p.png)
<br>
![](https://i.imgur.com/GQ2xUvo.png)
<br>

### 

### Security_Middleware
Security_Middleware提供許多種在request和response階段的安全性的強化方式,每個設定都可以獨立的設定

#### Request
在request真正被處理之前,進行安全行的檢測
* <b>SECURE_SSL_REDIRECT</b>
如果是True,則會將所有non-HTTPS的request重新導向到HTTPS
#### Response
在response回傳至使用者之前,在response中加上安全性的限制參數
* <b>SECURE_HSTS_SECONDS</b>
如果設立的值為非0數字,則會在所有沒有設定HTTP Strict Transport Security header的Response中加上他
* <b>SECURE_HSTS_![](https://i.imgur.com/9ZLnpww.png)INCLUDE_SUBDOMAINS</b>
如果是True,會將includeSubDomains 加到HTTP Strict Transport Security header. 假如SECURE_HSTS_SECONDS是設定非0整數,則才會有效 
* <b>SECURE_HSTS_PRELOAD</b>
如果是True,會將preload 加到HTTP Strict Transport Security header. 假如SECURE_HSTS_SECONDS是設定非0整數,則才會有效 
* <b>SECURE_CONTENT_TYPE_NOSNIFF</b>
如果設立的值為非0數字,則會在所有沒有設定 X-Content-Type-Options: nosniff header中的Response加上他 

## Request Object

## Response Object
### HttpResponse
#### Attribute
* HttpResponse.content
    * 利用proerty decorator將function包成的變數,主要是儲存要回傳給使用者的內容,為bytes型態 
* HttpResponse.status_code
    * response的HTTP status code,為整數型態,預設值為200,會透過reason_phrase來取得status code的constant
* HttpResponse.reason_phrase
    * 利用proerty decorator將function包成的變數,可以根據status_code的值取得相對應的HTTP constant
#### Method
* HttpResponse.\_\_setitem__(header,value):
    * 讓HttpResponse Object可以利用類似keyvalue的方式修改response header的值
* HttpResponse.\_\_getitem__(header):
    * 讓HttpResponse Object可以利用類似keyvalue的方式透過header key取得response header的值
* HttpResponse.\_\_len__():
    * 回傳response content的大小
* HttpResponse.make_bytes(value):
    * 將response content轉換成bytes的型態
    
## Url Router Structure
***
![](https://i.imgur.com/9ZLnpww.png)
#### 1. ExtractViewFromUrlPatterm depends on different url return different view function
#### 2. Setting your url handler and view (customize) in app directory (for user)
#### 3. Definded extractViewFromUrlPattern and path in utils.py
