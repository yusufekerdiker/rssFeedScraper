import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import {HttpClientModule} from "@angular/common/http";
import { HomeComponent } from './components/home/home.component';
import { DenemeComponent } from './components/deneme/deneme.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import {MatPaginatorModule} from '@angular/material/paginator';
import { HeaderComponent } from './components/header/header.component';
import { NewsProviderComponent } from './components/news-provider/news-provider.component';
import { CategoriesComponent } from './components/categories/categories.component';

import {MatDividerModule} from '@angular/material/divider';

import {MatIconModule} from '@angular/material/icon';
import { SortButtonComponent } from './components/sort-button/sort-button.component';

import {MatButtonModule} from '@angular/material/button';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    DenemeComponent,
    HeaderComponent,
    NewsProviderComponent,
    CategoriesComponent,
    SortButtonComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatPaginatorModule,
    MatDividerModule,
    MatIconModule,
    MatButtonModule,
  ],
  providers: [{
    provide: 'apiUrl',
    useValue: 'https://rssfeedscraper.onrender.com/'
}],
  bootstrap: [AppComponent]
})
export class AppModule { }
