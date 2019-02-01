import { Component, OnInit } from '@angular/core';
import { InitService } from './init.service';
import { HostListener } from '@angular/core';

import * as $ from 'jquery';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
	title = this.initService.title;
	
	innerHeight: number;

  constructor(private initService: InitService) { }

  @HostListener('window:resize', ['$event'])onResize(event) {
		this.tempResize();
	}
	

	tempResize() {
		this.innerHeight = window.innerHeight;
		if (this.innerHeight < 900) {
			$('body').append("<meta content='width=device-width, initial-scale=0.85, maximum-scale=0.85, user-scalable=0' name='viewport' />");
		}
	}

  ngOnInit() {
    this.tempResize();
	}
}