import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs/';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material';
import { InitService } from './init.service';
import { environment } from '../environments/environment.prod';
import { User } from './models/user';
import { Register } from './models/register';
// import { Message } from './models/message';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  DjangoAPI:string = environment.DjangoAPI;

  private userSource = new BehaviorSubject<User>(new User());
  user = this.userSource.asObservable();

  set userAccount(user: User) {
    localStorage.setItem('account', JSON.stringify(user));
    this.userSource.next(user);
  }

  constructor(private http: HttpClient, private router: Router, private initService: InitService) { }
  
  private getToken() {
    const token = localStorage.getItem('token');
    const httpHeaders = new HttpHeaders(
      {
        'content-type': 'application/json; charset=utf-8',
        'Authorization': 'Token ' + token
      });
      return {headers: httpHeaders};
  }

  userRegister(registerData: Register):Observable<any> {
    console.log(registerData);
    return this.http.post(this.DjangoAPI + "users/", registerData);
  }

  userLogin(userData: any):Observable<any> {
    return this.http.post(this.DjangoAPI + "authenticate/", userData);
  }

  getLoggedInUser():Observable<any> {
    return this.http.get(this.DjangoAPI + "users/loggedinuser/", this.getToken());
  }

  // Move those to a chat service later

  getLastChat(user_id: any):Observable<any> {
    const params = new HttpParams().set('user_id', user_id);
    return this.http.get(this.DjangoAPI + "chats/lastChat/?" + params, this.getToken());
  }

  getChatMessages(user_id: any, chat_id: any):Observable<any> {
    const params = new HttpParams().set('user_id', user_id).set('chat_id', chat_id);
    return this.http.get(this.DjangoAPI + "messages/chatMessages/?" + params, this.getToken());
  }

  sendMessage(params: any):Observable<any> {
    return this.http.post(this.DjangoAPI + "messages/sendMessage/", params, this.getToken());
  }

  getFriends(user_id: any):Observable<any> {
    const params = new HttpParams().set('user_id', user_id);
    return this.http.get(this.DjangoAPI + "users/friends/?" + params, this.getToken());
  }

  newChat(params: any):Observable<any> {
    return this.http.post(this.DjangoAPI + "chats/newChat/", params, this.getToken());
  }
}