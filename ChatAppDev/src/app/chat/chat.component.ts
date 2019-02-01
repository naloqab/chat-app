import { Component, OnInit, ChangeDetectorRef, ElementRef, ViewChild, AfterViewChecked } from '@angular/core';
import { trigger, style, transition, animate, keyframes, query, stagger } from '@angular/animations';
import { MaterialModule } from '../material.module';
import { FormBuilder, FormGroup } from '@angular/forms';
import { MediaMatcher } from '@angular/cdk/layout';
import { HttpClient, HttpParams } from '@angular/common/http';
import { UserService } from '../user.service';
import { InitService } from '../init.service';
import { Router } from '@angular/router';
import { HttpHeaders } from '@angular/common/http';
import { Title } from '@angular/platform-browser';
import { environment } from '../../environments/environment.prod';
// import { PushNotificationService } from 'ng-push-notification';

import * as $ from 'jquery';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css'],
  animations: [
	  trigger('messages', [
		transition('* => *', [
			query(':enter', style({ opacity: 0 }), { optional: true }),
			
			query(':enter', stagger('300ms', [
				animate('.6s ease-in', keyframes([
					style({ opacity: 0, transform: 'translateY(-75%)', offset: 0 }),
					style({ opacity: .5, transform: 'translateY(35px)', offset: .3 }),
					style({ opacity: 1, transform: 'translateY(0)', offset: 1 }),
				]))
			]), { optional: true }),
			
			query(':leave', stagger('300ms', [
				animate('.6s ease-in', keyframes([
					style({ opacity: 1, transform: 'translateY(0)', offset: 0 }),
					style({ opacity: .5, transform: 'translateY(35px)', offset: .3 }),
					style({ opacity: 0, transform: 'translateY(-75%)', offset: 1 }),
				]))
			]), { optional: true })
		])
	  ])
  ]
})

export class ChatComponent implements OnInit {

	// @ViewChild('text-box') private elementRef: ElementRef;
	
	// @ViewChild('scrollMe') private myScrollContainer: ElementRef;

	// scrollToBottom(): void {
	// 		try {
	// 				this.myScrollContainer.nativeElement.scrollTop = this.myScrollContainer.nativeElement.scrollHeight;
	// 		} catch(err) { }                 
	// }
  
  logout() {
		localStorage.clear();
		this.router.navigate(['chat/login']);
	}

	playAudio(direction) {
		let audio = new Audio();
		if (direction == "incoming") {
			// audio.src = "./media/quite-impressed.mp3";
			audio.src = environment.mediaURL + "quite-impressed.mp3";
		}
		else {
			// audio.src = "./media/just-like-that.mp3";
			audio.src = environment.mediaURL + "just-like-that.mp3";
		}
		audio.load();
		// setTimeout(() => {
		audio.play();
		// }, 500);
	}

	getLoggedinUser() {
		const userAccount = JSON.parse(localStorage.getItem('account'));
		if (!userAccount) {
			console.log('User not logged in. Redirecting to login page.');
			this.router.navigate(['chat/login']);
		}
		else {
			this.getLastChat();
			// console.log(JSON.parse(userAccount));
		}
	}

	chat_id:any = null;
	
  getLastChat() {
		const userAccount = JSON.parse(localStorage.getItem('account'));
    this.userService.getLastChat(userAccount.id).subscribe(
      response => {
				this.chat_id = response.chat_id;
				this.getMessages();
				this.getFriends();
      },
      error => {
        console.log(error);
      }
    );
	}
	
	friendUserInfo:any;
	messageObjects:any = [];
	
  getMessages() {
		const userAccount = JSON.parse(localStorage.getItem('account'));
    this.userService.getChatMessages(userAccount.id, this.chat_id).subscribe(
      response => {
				this.friendUserInfo = response.friendUserInfo;
				this.messageObjects = response.messageObjects;
				this.newMessage();
      },
      error => {
        console.log(error);
				this.router.navigate(['chat/login']);
      }
    );
  }

	pageLoadTime: Date = new Date();
	currentTime: Date = this.pageLoadTime;

	previousMessageObjectTime: Date;
	
	newMessage() {
		const userAccount = JSON.parse(localStorage.getItem('account'));
		if (this.pageLoadTime != this.currentTime) {
			if (this.messageObjects != []) {
				if (this.previousMessageObjectTime != this.messageObjects[this.messageObjects.length-1].time) {
					if (this.messageObjects[this.messageObjects.length-1].username != userAccount.username) {
						if ('Notification' in window && (Notification as any).permission == 'granted') {
							if (document.visibilityState != 'hidden') {
								this.playAudio("incoming");
							}
						}
						else {
							this.playAudio("incoming");
						}
						this.titleService.setTitle("You have a new message from " + this.friendUserInfo.first_name + "!");
						this.sendNewNotification();
						// this.pushNotification.show("You have a new message from " + this.friendFirstName + "!");
					}
					else {
						this.playAudio("outgoing");
						this.titleService.setTitle("ChatApp");
					}
					if (this.messageObjects != []) {
						this.previousMessageObjectTime = this.messageObjects[this.messageObjects.length-1].time;
					}
					// this.scrollToLastMessage();
					// this.scrollToBottom();
				}
			}
		}
		else {
			this.currentTime = new Date();
			if (this.messageObjects != []) {
				this.previousMessageObjectTime = this.messageObjects[this.messageObjects.length-1].time;
			}
		}
	}
	
	messageContent:any = '';

	sendMessageParams:any;
	
  sendMessage() {
		if (this.chat_id != null) {
			const userAccount = JSON.parse(localStorage.getItem('account'));
			this.sendMessageParams = {user_id: userAccount.id, chat_id: this.chat_id, messageContent: this.messageContent};
			this.userService.sendMessage(this.sendMessageParams).subscribe(
				response => {
					this.messageContent = "";
					this.getMessages();
				},
				error => {
					console.log(error); 
				}
			);
		}
		else {
			this.messageContent = "";
			// alert("You have not added any friends.");
			console.log("User has not added any friends.");
		}
  }
	
	friends:any;

	getFriends() {
		const userAccount = JSON.parse(localStorage.getItem('account'));
    this.userService.getFriends(userAccount.id).subscribe(
      response => {
				this.friends = response.friends;
      },
      error => {
        console.log(error);
				this.router.navigate(['chat/login']);
      }
    );
	}
	
	friendsList:any;
	friendSearched:string;


	searchFriend() {
		this.newChat(this.friendSearched);
	}

	selectFriend(friendUsername: string) {
		this.newChat(friendUsername);
	}
	
	newChat(friendUsername: string) {
		// this.elementRef.nativeElement.focus();
		this.pageLoadTime = new Date();
		this.currentTime = this.pageLoadTime;
		const userAccount = JSON.parse(localStorage.getItem('account'));
		const params = {username: userAccount.username, friend_username: friendUsername};
    this.userService.newChat(params).subscribe(
      response => {
				this.chat_id = response.chat_id;
				this.getMessages();
      },
      error => {
        console.log(error);
      }
    );
		this.friendSearched = "";
	}
	getNotificationPermission(){
		if ('Notification' in window && (Notification as any).permission != 'granted') {
			(Notification as any).requestPermission();
		}
	}

	sendNewNotification() {
		if ((Notification as any).permission == 'granted' && document.visibilityState == 'hidden') {
			const notification = new Notification('You have a new message from ' + this.friendUserInfo.first_name + '!');
		}
	}

	delay(ms: number) {
		return new Promise( resolve => setTimeout(resolve, ms) );
	}


	// checkOtherChats() {
	// 	var method = 'check_other_chats';
	// 	const params = new HttpParams().set('method', method);
	// 	this.http.get(this.initService.DjangoAPI, {params}).subscribe(returned_data => {
	//   if (returned_data['success']) {
	// 			this.friends = returned_data['friends'];
	// 		}
	// 		else {
	// 			console.log(method + ": " + returned_data['message']);
	// 		}
	// 	},
	// 	err => {
	// 		this.initService.unexpectedError(method);
	// 	});
	// }




  mobileQuery: MediaQueryList;

  private _mobileQueryListener: () => void;

  constructor(changeDetectorRef: ChangeDetectorRef, media: MediaMatcher, private http: HttpClient, private userService: UserService, private initService: InitService, private router: Router, private titleService: Title) {
		this.mobileQuery = media.matchMedia('(max-width: 600px)');
		this._mobileQueryListener = () => changeDetectorRef.detectChanges();
		this.mobileQuery.addListener(this._mobileQueryListener);
	}
	
	getMessagesLoop:any;

	ngOnInit() {
		this.getLoggedinUser();
		
		this.getMessagesLoop = setInterval( () => {
			this.getMessages();
		}, 5000);

		this.getNotificationPermission();
		// setInterval( () => { 
		// 	this.checkOtherChats();
		// }, 1000 );
		// this.scrollToBottom();
	}

	// ngAfterViewChecked() {
	// 		this.scrollToBottom();
	// } 
	
  ngOnDestroy(): void {
	this.mobileQuery.removeListener(this._mobileQueryListener);
	clearInterval(this.getMessagesLoop);
  }
}