# Quote Maker

Just another python script to automate boring stuff. Quote maker easy to create a quoted image and publish to a Facebook page. 

#### Depended Python libs

-Pillow

### Install 
**manual**
```sh
pip3 install --upgrade -r requirements.txt"
python quote_maker/main.py
```

**pypi**
```sh
pip3 install quote-maker
```

#### Depended libs

    * curl 7.52.1 (x86_64-pc-linux-gnu) 
    * libcurl/7.52.1 
    * OpenSSL/1.0.2l 
    * zlib/1.2.8

### Run

run the script by 

    $:python3.6 main.py
    ****************************************************************************************
    ​~~~ quote_maker.py ~~~
    quote: Infinite love is the only truth. Everything else is illusion. David Icke

### Output

![](images/de201299-1307-4b94-856a-da362ea1f1ce.png)
![](images/406a9722-67fd-4365-b2a1-70dfb5e393e3.png)
![](images/95128597-da6a-4b4f-af1b-457b452f22d5.png) 
![](images/8f7e289e-c782-4c4e-af29-9d8b70d4170e.png)
![](images/9f4bad89-69a6-4cfb-af53-38f64bbd9d99.png)

### Post to Facebook

To enable access of Facebook to publish, following variable has to be hardcoded to achieve. 

`page_id`  - facebook page ID, information can obtain from the page about. if you want to post on the personal wall 

just hardcode `page_id` = "me".

`facebook_token` - facebook access token with publish_action enable. for more visit

 Graph API explorer: https://developers.facebook.com/tools/explorer/145634995501895/

Please uncomment #os.system(command) in main.py

### How to change image size?

`image_size_x` `image_size_y` responcible for image size.



###### Note: background colour is random, but the fourground colour is always white. 

