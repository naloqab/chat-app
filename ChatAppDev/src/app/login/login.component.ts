import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service';
import { InitService } from '../init.service';
import { Router } from '@angular/router';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html', 
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  title = 'ChatApp';

  userData: FormGroup;

  constructor(public initService: InitService, private userService: UserService, private router: Router, private formBuilder: FormBuilder) { 
    this.userData = this.formBuilder.group(
      {
        username: ['', Validators.required],
        password: ['', Validators.required],
      }
    );
  }

  ngOnInit() {
    if (localStorage.getItem('token')) {
      // this.router.navigate(['chat']);
    }
    this.initService.loading = false;
  }

  onLogin() {
    this.initService.loading = true;
    this.userService.userLogin(this.userData.value).subscribe(
      response => {
        localStorage.setItem('token', response.token);
        this.getLoggedInUser();
      },
      error => {
        console.log(error);
        // should be snickerbar
        alert(this.userData.value.username + " is not a registered user.");
      }
    );
    this.initService.loading = false;
  }

  getLoggedInUser() {
    this.userService.getLoggedInUser().subscribe(
      response => {
        this.userService.userAccount = response;
        this.router.navigate(['chat']);
      },
      error => {
        console.log(error);
      }
    );
  }
}