import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NewsService } from '../../services/news.service';
import { News, Article } from '../../models/news';
import { SortService } from 'src/app/services/sort.service';


@Component({
  selector: 'app-news-provider',
  templateUrl: './news-provider.component.html',
  styleUrls: ['./news-provider.component.scss']
})
export class NewsProviderComponent implements OnInit {
  publisher: string | null = null;  // The name of the publisher as retrieved from the URL
  articles: Article[] = [];  // An array to hold the articles data fetched from the NewsService

  changeSortingOrder: boolean = true;

  constructor(private newsService: NewsService, private route: ActivatedRoute, private sortService: SortService) {}

  // after creating component
  ngOnInit(): void {
    // Subscribe to any changes in the route parameters 
    // this is for checking link route like http://localhost:4200/publisher/CNET or http://localhost:4200/publisher/Wired
    this.route.paramMap.subscribe(params => {
      // Get the publisher parameter from the routing
      this.publisher = params.get('publisher');
      // Fetch articles from the specific publisher
      this.fetchArticles();
    });
  }

  //fetch articles from a specific publisher
  fetchArticles(): void {
    //check if a publisher was retrieved from the route
    if (this.publisher) {
      this.newsService.getNewsByPublisher(this.publisher).subscribe(articles => {
        this.articles = articles;
      });
    }
  }

  onSort(changeSortingOrder: boolean) {
    this.changeSortingOrder = changeSortingOrder;
    this.sortArticles();
  }
  

  sortArticles() {
    this.articles = this.sortService.sortArticles(
      this.articles,
      this.changeSortingOrder
    );
  }

  showAlert: boolean = false;
  alertMessage: string = '';
  alertType: string = '';

  handleAlert(event: { message: string; type: string }): void {
    this.showAlert = true;
    this.alertMessage = event.message;
    this.alertType = event.type;
    setTimeout(() => (this.showAlert = false), 3000);
  }
}
