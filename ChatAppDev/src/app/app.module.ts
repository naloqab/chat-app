import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';

// import {HttpXsrfCookieExtractor, HttpXsrfInterceptor, HttpXsrfTokenExtractor, XSRF_COOKIE_NAME, XSRF_HEADER_NAME} from './xsrf';

import { AppRoutingModule } from './app-routing.module';

import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { ChatComponent } from './chat/chat.component';

import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MaterialModule } from './material.module';

// import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { UserService } from './user.service';

import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { HttpXsrfInterceptor } from './interceptor';

import { CookieService } from 'ngx-cookie-service';

import { Title } from '@angular/platform-browser';

import { PushNotificationModule } from 'ng-push-notification';


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    ChatComponent
    // Sidenav
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    MaterialModule,
    HttpClientModule,
    // HttpClientXsrfModule,
    // HttpClientXsrfModule.withOptions({
    //   cookieName: 'csrftoken',
    //   headerName: 'X-CSRFToken',
    // }),
    // BehaviorSubject
    PushNotificationModule
  ],
  providers: [
    UserService,
    CookieService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
