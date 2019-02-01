import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { BehaviorSubject } from 'rxjs';
import { Router } from '@angular/router';
import { HttpHeaders } from '@angular/common/http';
import { MatSnackBar } from '@angular/material';

@Injectable({
  providedIn: 'root'
})
export class InitService {

  title = "Chat";
  loading: boolean;

  unexpectedError(method) {
    console.log(method + ": " + "Request error occured.");
    alert("An unexpected error has occured.");
  }

  constructor(private http: HttpClient, private router: Router) { }
}