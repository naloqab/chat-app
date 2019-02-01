import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service';
import { InitService } from '../init.service';
import { Router } from '@angular/router';
import { FormGroup, Validators, FormBuilder, FormControl, FormGroupDirective, NgForm } from '@angular/forms';
import { ErrorStateMatcher } from '@angular/material/core';

// import * as $ from 'jquery';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

	registerData: FormGroup;

	matcher = new MyErrorStateMatcher();
  
	constructor(public initService: InitService, private userService: UserService, private router: Router, private formBuilder: FormBuilder) { 
	  this.registerData = this.formBuilder.group(
		{
		  first_name: ['', Validators.required],
		  last_name: ['', Validators.required],
		  email: ['', Validators.required],
		  username: ['', [Validators.required]],
		  password: ['', [Validators.required, Validators.minLength(6)]],
		  confirmPassword: ['']
		}, {validator: this.checkPasswords }
	  );
	}

  ngOnInit() {
    if (localStorage.getItem('token')) {
      // this.router.navigate(['chat']);
    }
    this.initService.loading = false;
  }

  onRegister() {
    this.initService.loading = true;
    this.userService.userRegister(this.registerData.value).subscribe(
      response => {
				// console.log(response);
        this.router.navigate(['chat/login']);
      },
      error => {
        console.log(error);
				if (error.message.includes("1062")) {
					alert("You are already registered.");
					this.router.navigate(['chat/login']);
				}
      }
    );
    this.initService.loading = false;
	}

	checkPasswords(registerData: FormGroup) { // here we have the 'passwords' group
		let password = registerData.controls.password.value;
		let confirmPassword = registerData.controls.confirmPassword.value;

		return password === confirmPassword ? null : { notSame: true }     
	}
}

export class MyErrorStateMatcher implements ErrorStateMatcher {
  isErrorState(control: FormControl | null, form: FormGroupDirective | NgForm | null): boolean {
    const invalidCtrl = !!(control && control.invalid && control.parent.dirty);
    const invalidParent = !!(control && control.parent && control.parent.invalid && control.parent.dirty);

    return (invalidCtrl || invalidParent);
  }
}