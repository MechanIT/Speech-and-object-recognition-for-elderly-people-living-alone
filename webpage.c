// 라이브러리
// SSD1306 검색
// ESP8266 and ESP32 OLED driver for SSD1306 displays
// 버전 4.3.0
// wifi의 접속정보를 무작위로 발생하고 OLED에 wifi의 접속정보를 보여줌

//////////////// 라이브러리 import ////////////////
#include <WiFi.h> //무선 연결 라이브러리
#include <Wire.h> //I2C 통신 라이브러리
#include "SSD1306Wire.h"     //OLED 디스플레이 제어 라이브러리
#include "EEPROM.h"
#include "esp_camera.h"
#include "esp_timer.h"
#include "img_converters.h"
#include "Arduino.h"
#include "fb_gfx.h"
#include "soc/soc.h"             
#include "soc/rtc_cntl_reg.h"  
#include "esp_http_server.h"

//////////////// 변수 설정 ////////////////
int car_speed = map(40,0,100,0,255); //차량 속도를 40으로 설정, 0~100의 속도를 0~255로 매핑

#define SSID_EEP_ADDR 0

#define IN_11 12
#define IN_12 13
#define IN_21 15
#define IN_22 14

#define PART_BOUNDARY "123456789000000000000987654321"

#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27

#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

SSD1306Wire display(0x3c, 0, 2, GEOMETRY_128_32);

//////////////// 스트리밍과 HTTPD 관련 설정 ////////////////

//MIME 타입 정의 -> 웹 페이지에서 카메라로부터 스트리밍 영상을 연속적으로 받기 위함
static const char* _STREAM_CONTENT_TYPE = "multipart/x-mixed-replace;boundary=" PART_BOUNDARY;

//스트리밍 데이터 각 부분을 구분하는 경계선을 정의
static const char* _STREAM_BOUNDARY = "\r\n--" PART_BOUNDARY "\r\n";

//스트리밍 데이터 각 부분을 구성하는 헤더 정의. 컨텐츠 타입과 길이 정의
static const char* _STREAM_PART = "Content-Type: image/jpeg\r\nContent-Length: %u\r\n\r\n";

//두 개의 웹서버 핸들 정의
httpd_handle_t camera_httpd = NULL; //일반 웹 요청 처리
httpd_handle_t stream_httpd = NULL; //영상 스트리밍을 위

//////////////// HTML 페이지 설정 ////////////////
static const char PROGMEM INDEX_HTML[] = R"rawliteral(
<html>
  <head>
    <title> AI CAR</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      body { font-family: Arial; text-align: center; margin:0px auto; padding-top: 30px;}
      table { margin-left: auto; margin-right: auto; }
      td { padding: 8 px; }
      .button {
        background-color: #2f4468;
        border: none;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 18px;
        margin: 6px 3px;
        cursor: pointer;
        -webkit-touch-callout: none;
        -webkit-user-select: none;
        -khtml-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        -webkit-tap-highlight-color: rgba(0,0,0,0);
      }
      img {  width: auto ;
        max-width: 100% ;
        height: auto ; 
      }
    </style>
  </head>
  <body>
    <h1>Sookmyung AI CAR</h1>
    <img src="" id="photo" >
<table>
  <div align="center">
  <button class="button" onmousedown="toggleCheckbox('speed40');" ontouchstart="toggleCheckbox('speed40');">Speed 40</button>
  <button class="button" onmousedown="toggleCheckbox('speed50');" ontouchstart="toggleCheckbox('speed50');">Speed 50</button>
  <button class="button" onmousedown="toggleCheckbox('speed60');" ontouchstart="toggleCheckbox('speed60');">Speed 60</button>
  <button class="button" onmousedown="toggleCheckbox('speed80');" ontouchstart="toggleCheckbox('speed80');">Speed 80</button>
  <button class="button" onmousedown="toggleCheckbox('speed100');" ontouchstart="toggleCheckbox('speed100');">Speed 100</button>
  </div>
  
  <tr>
    <td colspan="6" align="center">
      <button class="button" onmousedown="toggleCheckbox('forward');" ontouchstart="toggleCheckbox('forward');" onmouseup="toggleCheckbox('stop');" ontouchend="toggleCheckbox('stop');">Forward</button>
    </td>
  </tr>
  <tr>
    <td align="center">
      <button class="button" onmousedown="toggleCheckbox('turn_left');" ontouchstart="toggleCheckbox('turn_left');" onmouseup="toggleCheckbox('stop');" ontouchend="toggleCheckbox('stop');">Turn Left</button>
    </td>
    <td align="center">
      <button class="button" onmousedown="toggleCheckbox('left');" ontouchstart="toggleCheckbox('left');" onmouseup="toggleCheckbox('stop');" ontouchend="toggleCheckbox('stop');">Left</button>
    </td>
    <td align="center">
      <button class="button" onmousedown="toggleCheckbox('stop');" ontouchstart="toggleCheckbox('stop');">Stop</button>
    </td>
    <td align="center">
      <button class="button" onmousedown="toggleCheckbox('right');" ontouchstart="toggleCheckbox('right');" onmouseup="toggleCheckbox('stop');" ontouchend="toggleCheckbox('stop');">Right</button>
    </td>
    <td align="center">
      <button class="button" onmousedown="toggleCheckbox('turn_right');" ontouchstart="toggleCheckbox('turn_right');" onmouseup="toggleCheckbox('stop');" ontouchend="toggleCheckbox('stop');">Turn Right</button>
    </td>
  </tr>
  <tr>
    <td colspan="6" align="center">
      <button class="button" onmousedown="toggleCheckbox('backward');" ontouchstart="toggleCheckbox('backward');" onmouseup="toggleCheckbox('stop');" ontouchend="toggleCheckbox('stop');">Backward</button>
    </td>
  </tr>
</table>

   <script>
   function toggleCheckbox(x) {
     var xhr = new XMLHttpRequest();
     xhr.open("GET", "/action?go=" + x, true);
     xhr.send();
   }
   window.onload = document.getElementById("photo").src = window.location.href.slice(0, -1) + ":81/stream";
  </script>
  </body>
</html>
)rawliteral";

static esp_err_t index_handler(httpd_req_t *req){   //웹 페이지에 대한 HTTP 요청 처리. 웹 페이지의 HTML 내용을 클라이언트로 보냄
  httpd_resp_set_type(req, "text/html");  //응답의 MIME 타입을 "text/html"로 설정
  return httpd_resp_send(req, (const char *)INDEX_HTML, strlen(INDEX_HTML));  //저장된 HTML 내용을 보내 웹 브라우저에 표시
}

static esp_err_t stream_handler(httpd_req_t *req){  //카메라 스트리밍 요청 처리. 카메라로부터 연속적인 이미지 프레임을 받아 클라이언트로 보냄
  camera_fb_t * fb = NULL;
  esp_err_t res = ESP_OK;
  size_t _jpg_buf_len = 0;
  uint8_t * _jpg_buf = NULL;
  char * part_buf[64];

  res = httpd_resp_set_type(req, _STREAM_CONTENT_TYPE);
  if(res != ESP_OK){
    return res;
  }

  while(true){
    fb = esp_camera_fb_get();
    if (!fb) {
      Serial.println("Camera capture failed");
      res = ESP_FAIL;
    } else {
      if(fb->width > 400){
        if(fb->format != PIXFORMAT_JPEG){
          bool jpeg_converted = frame2jpg(fb, 80, &_jpg_buf, &_jpg_buf_len);
          esp_camera_fb_return(fb);
          fb = NULL;
          if(!jpeg_converted){
            Serial.println("JPEG compression failed");
            res = ESP_FAIL;
          }
        } else {
          _jpg_buf_len = fb->len;
          _jpg_buf = fb->buf;
        }
      }
    }
    if(res == ESP_OK){
      size_t hlen = snprintf((char *)part_buf, 64, _STREAM_PART, _jpg_buf_len);
      res = httpd_resp_send_chunk(req, (const char *)part_buf, hlen);
    }
    if(res == ESP_OK){
      res = httpd_resp_send_chunk(req, (const char *)_jpg_buf, _jpg_buf_len);
    }
    if(res == ESP_OK){
      res = httpd_resp_send_chunk(req, _STREAM_BOUNDARY, strlen(_STREAM_BOUNDARY));
    }
    if(fb){
      esp_camera_fb_return(fb);
      fb = NULL;
      _jpg_buf = NULL;
    } else if(_jpg_buf){
      free(_jpg_buf);
      _jpg_buf = NULL;
    }
    if(res != ESP_OK){
      break;
    }
    //Serial.printf("MJPG: %uB\n",(uint32_t)(_jpg_buf_len));
  }
  return res;
}

static esp_err_t cmd_handler(httpd_req_t *req){ //클라이언트로부터 오는 명령어 처리 -> 자동차 방향, 속도 조절
  char*  buf;
  size_t buf_len;
  char variable[32] = {0,};
  
  buf_len = httpd_req_get_url_query_len(req) + 1;
  if (buf_len > 1) {
    buf = (char*)malloc(buf_len);
    if(!buf){
      httpd_resp_send_500(req);
      return ESP_FAIL;
    }
    if (httpd_req_get_url_query_str(req, buf, buf_len) == ESP_OK) { //URL 쿼리 문자열 추출
      if (httpd_query_key_value(buf, "go", variable, sizeof(variable)) == ESP_OK) { //쿼리에서 특정 키 'go'에 대한 값 추출
      } else {
        free(buf);
        httpd_resp_send_404(req);
        return ESP_FAIL;
      }
    } else {
      free(buf);
      httpd_resp_send_404(req);
      return ESP_FAIL;
    }
    free(buf);
  } else {
    httpd_resp_send_404(req);
    return ESP_FAIL;
  }

  sensor_t * s = esp_camera_sensor_get();
  int res = 0;
  
  if(!strcmp(variable, "forward")) {  //쿼리에서 받아온 값이 'forward'일 경우에 다음을 실행
    Serial.println("Forward");  //시리얼에 출력
    car_go(car_speed);  //직진 함수 실행
  }
  else if(!strcmp(variable, "left")) {
    Serial.println("Left");
    car_go_left(car_speed);
  }
  else if(!strcmp(variable, "right")) {
    Serial.println("Right");
    car_go_right(car_speed);
  }
  else if(!strcmp(variable, "turn_left")) {
    Serial.println("Turn Left");
    car_turn_left(car_speed);
  }
  else if(!strcmp(variable, "turn_right")) {
    Serial.println("Turn Right");
    car_turn_right(car_speed);
  }
  else if(!strcmp(variable, "backward")) {
    Serial.println("Backward");
    car_back(car_speed);
  }
  else if(!strcmp(variable, "stop")) {
    Serial.println("Stop");
    car_go(0);
  }
  else if(!strcmp(variable, "speed40")) {
    Serial.println("speed40");
    car_speed = map(40,0,100,0,255); //40%의속도로 설정
    Serial.println(car_speed);
  }
  else if(!strcmp(variable, "speed50")) {
    Serial.println("speed50");
    car_speed = map(50,0,100,0,255); //50%의속도로 설정
    Serial.println(car_speed);
  }
  else if(!strcmp(variable, "speed60")) {
    Serial.println("speed60");
    car_speed = map(60,0,100,0,255); //60%의속도로 설정
    Serial.println(car_speed);
  }
  else if(!strcmp(variable, "speed80")) {
    Serial.println("speed80");
    car_speed = map(80,0,100,0,255); //80%의속도로 설정
    Serial.println(car_speed);
  }
  else if(!strcmp(variable, "speed100")) {
    Serial.println("speed100");
    car_speed = map(100,0,100,0,255); //100%의속도로 설정
    Serial.println(car_speed);
  }
  else {
    res = -1;
  }

  if(res){
    return httpd_resp_send_500(req);  //Internal Server Error를 뜻하는 상태 코드 500을 클라이언트에 응답
  }

  httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");
  return httpd_resp_send(req, NULL, 0);
}

void startCameraServer(){         // 웹서버 설정 및 시작하는 함수
  httpd_config_t config = HTTPD_DEFAULT_CONFIG();   //HTTP 서버에 대한 기본 설정 초기화
  config.server_port = 80;  //서버 포트 번호

  // URI 핸들러 등록. URI : 명렁 처리를 위한 경로, 핸들러 : 서버가 특정 URL 경로에 대한 요청을 받았을 때, 어떻게 반응할 지 결정
  httpd_uri_t index_uri = {     //웹페이지 요청을 처리하기 위함
    .uri       = "/",
    .method    = HTTP_GET,
    .handler   = index_handler,
    .user_ctx  = NULL
  };

  httpd_uri_t cmd_uri = {       //명령어를 처리하기 위함
    .uri       = "/action",
    .method    = HTTP_GET,
    .handler   = cmd_handler,
    .user_ctx  = NULL
  };
  httpd_uri_t stream_uri = {    //카메라 스트리밍을 처리하기 위함
    .uri       = "/stream",
    .method    = HTTP_GET,
    .handler   = stream_handler,
    .user_ctx  = NULL
  };
  if (httpd_start(&camera_httpd, &config) == ESP_OK) {    //웹서버 시작 명령어
    httpd_register_uri_handler(camera_httpd, &index_uri);
    httpd_register_uri_handler(camera_httpd, &cmd_uri);
  }
  //스트리밍 서버는 별도의 포트를 사용함
  config.server_port += 1;
  config.ctrl_port += 1;
  if (httpd_start(&stream_httpd, &config) == ESP_OK) {  //스트리밍 서버 시작 명령어
    httpd_register_uri_handler(stream_httpd, &stream_uri);
  }
}

void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); //disable brownout detector
  
  pinMode(IN_11,OUTPUT);
  pinMode(IN_12,OUTPUT);
  pinMode(IN_21,OUTPUT);
  pinMode(IN_22,OUTPUT);
  
  Serial.begin(115200);   //baudrate 115200으로 설정
  Serial.setDebugOutput(false);
  
  //EEPROM 초기화
  EEPROM.begin(10); //EEPROM 라이브러리 초기화, 10바이트의 공간 사용 -> 나중에 이 공간에 SSID 정보가 저장됨
  String read_eep_ssid = EEPROM.readString(SSID_EEP_ADDR);  //EEPROM에서 지정된 주소 (SSID_EEP_ADDR)을 읽어옴 = 와이파이 SSID로 사용

  if (read_eep_ssid.indexOf("car") >= 0) {  //SSID 문자열에 'car'라는 문자열이 포함되어 있는지 확인
    Serial.println(read_eep_ssid);  //있으면 SSID 출력
  }
  else { //초기에 eeprom에 데이터가 없다면 car100000~car999999 까지 랜덤한 ID를 부여한다
    Serial.println("eep write");
    int rand_num = random(100000, 999999);
    String eep_write_string = "car" + String(rand_num);
    EEPROM.writeString(SSID_EEP_ADDR, eep_write_string);  //새롭게 만든 SSID를 EEPROM의 'SSID_EEP_ADDR'이라는 주소에 저장
    EEPROM.commit();  //변경사항을 EEPROM에 확실히 저

    String read_eep_ssid = EEPROM.readString(SSID_EEP_ADDR);
  }
  
  //OLED 초기화
  display.init();

  display.flipScreenVertically();
  display.setFont(ArialMT_Plain_16);
  display.setTextAlignment(TEXT_ALIGN_LEFT);

  //wifi 연결
  const char* ssid = read_eep_ssid.c_str();
  WiFi.begin(ssid, "123456789");  //SSID와 고정된 비밀번호 "123456789"를 사용하여 와이파이 연결 시도

  //디스플레이에 SSID, 비밀번호 표시
  int wifi_status = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    if(wifi_status == 0){
      display.clear();
      display.drawString(0, 0, "SSID:");
      display.drawString(40, 0, ssid);
      display.drawString(0, 16, "PASS:");
      display.drawString(45, 16, "123456789");
      display.display();
    }
    else{
      display.clear();
      display.drawString(0, 0, "SSID:");
      display.drawString(40, 0, ssid);
      display.drawString(120, 0, ".");
      display.drawString(0, 16, "PASS:");
      display.drawString(45, 16, "123456789");
      display.display();
    }
    
    wifi_status = !wifi_status;
  }

  //OLED에 IP주소 표시
  display.clear();
  display.drawString(20, 0, "IP address:");
  display.drawString(0, 16, ip2Str(WiFi.localIP()));
  display.display();

  //camera 초기화
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG; 
  
  if(psramFound()){
    config.frame_size = FRAMESIZE_VGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }
  
  // Camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  //웹서버 시작
  startCameraServer();
}

void loop() {
  
}

String ip2Str(IPAddress ip){
  String s="";
  for (int i=0; i<4; i++) {
    s += i  ? "." + String(ip[i]) : String(ip[i]);
  }
  return s;
}

void car_go(int speed){
  //오른쪽모터
  digitalWrite(IN_11,HIGH);
  analogWrite(IN_12,speed);
  
  //왼쪽모터
  digitalWrite(IN_21,LOW);
  analogWrite(IN_22,speed);
}

void car_back(int speed){
  //오른쪽모터
  digitalWrite(IN_11,LOW);
  analogWrite(IN_12,speed);
  
  //왼쪽모터
  digitalWrite(IN_21,HIGH);
  analogWrite(IN_22,speed);
}

void car_go_left(int speed){
  //오른쪽모터
  digitalWrite(IN_11,HIGH);
  analogWrite(IN_12,speed);
  
  //왼쪽모터
  digitalWrite(IN_21,HIGH);
  analogWrite(IN_22,0);
}

void car_go_right(int speed){
  //오른쪽모터
  digitalWrite(IN_11,LOW);
  analogWrite(IN_12,0);
  
  //왼쪽모터
  digitalWrite(IN_21,LOW);
  analogWrite(IN_22,speed);
}

void car_turn_left(int speed){
  //오른쪽모터
  digitalWrite(IN_11,HIGH);
  analogWrite(IN_12,speed);
  
  //왼쪽모터
  digitalWrite(IN_21,HIGH);
  analogWrite(IN_22,speed);
}

void car_turn_right(int speed){
  //오른쪽모터
  digitalWrite(IN_11,LOW);
  analogWrite(IN_12,speed);
  
  //왼쪽모터
  digitalWrite(IN_21,LOW);
  analogWrite(IN_22,speed);
}
