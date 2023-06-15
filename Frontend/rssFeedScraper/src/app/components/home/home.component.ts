import { Component, OnInit, ViewChild } from '@angular/core';
import { NewsService } from '../../services/news.service';
import { News, Article } from '../../models/news';

import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { SortService } from 'src/app/services/sort.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
  allArticles: Article[] = []; // store all articles from api
  changeSortingOrder: boolean = true; // bool variable from change sorting and for its button

  // pagination stuff https://material.angular.io/components/paginator/examples#paginator-configurable
  length = 0; //total number of articles
  pageSize = 8; //articles shown per page
  pageSizeOptions: number[] = [8, 16, 24, 32, 40]; //option for changing number of articles shown per page
  pageIndex = 0; // our current page index
  paginatedArticles: Article[] = []; //articles in our current page

  constructor(
    private newsService: NewsService,
    private sortService: SortService
  ) {}

  //import pagination ui from angular mat
  @ViewChild(MatPaginator) paginator: MatPaginator | undefined;

  ngOnInit() {
    this.getNews();
  }

  getNews(): void {
    this.newsService.getNews().subscribe((data: News) => {
      //subscribe and or listen the api and get items from it when change happens
      for (const publisher in data) {
        this.allArticles = this.allArticles.concat(data[publisher]);
      }
      this.length = this.allArticles.length; //update the total no of articles for showing in pagination ui
      this.sortArticles(); //sort articles
      this.getPaginatedItems(); //get news for our current paginated page
    });
  }

  getPaginatedItems() {
    //calculate the index where we should start slicing the array of articles list
    let startIndex = this.pageIndex * this.pageSize;
    //get a slice of the array that shows to the current page
    this.paginatedArticles = this.allArticles.slice(
      startIndex,
      startIndex + this.pageSize
    );
  }

  //when the user changes page update the page index/number and size then get the articles for the new page
  handlePage(e: PageEvent) {
    this.pageIndex = e.pageIndex;
    this.pageSize = e.pageSize;
    this.getPaginatedItems();
  }

  //when the user wants to change the sorting order we flip the bool value of changeSortingOrder, sort the articles and get the articles for the current page
  onSort(changeSortingOrder: boolean) {
    this.changeSortingOrder = changeSortingOrder;
    this.sortArticles();
    this.getPaginatedItems();
  }

  //in here we sort the articles array. Depending on the bool value of changeSortingOrder, we sort by date in ascending or descending order
  sortArticles() {
    this.allArticles = this.sortService.sortArticles(
      this.allArticles,
      this.changeSortingOrder
    ); // Use the service to sort
  }
}
