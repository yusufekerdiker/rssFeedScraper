import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import {HttpClientModule} from "@angular/common/http";
import { HomeComponent } from './components/home/home.component';
import { DenemeComponent } from './components/deneme/deneme.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    DenemeComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule
  ],
  providers: [{
    provide: 'apiUrl',
    useValue: 'https://deneme-35ra.onrender.com/api/data'
}],
  bootstrap: [AppComponent]
})
export class AppModule { }
