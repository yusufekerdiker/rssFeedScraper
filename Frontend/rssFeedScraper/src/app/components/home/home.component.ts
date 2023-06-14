import { Component, OnInit } from '@angular/core';
import { NewsService } from '../../services/news.service';
import { News, Article } from '../../models/news';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
  allArticles: Article[] = [];
  changeSortingOrder: boolean = true;

  constructor(private newsService: NewsService) {}

  ngOnInit() {
    this.newsService.getNews().subscribe((data: News) => {
      for (const publisher in data) {
        this.allArticles = this.allArticles.concat(data[publisher]);
      }
      this.sortArticles();
    });
  }

  toggleSort() {
    this.changeSortingOrder = !this.changeSortingOrder;
    this.sortArticles();
  }

  sortArticles() {
    this.allArticles.sort((a, b) => {
      if (this.changeSortingOrder) {
        return new Date(b.publishDate).getTime() - new Date(a.publishDate).getTime();
      } else {
        return new Date(a.publishDate).getTime() - new Date(b.publishDate).getTime();
      }
    });
  }


  switchTheme(): void {
    const currentTheme = document.documentElement.getAttribute('data-bs-theme');
    document.documentElement.setAttribute('data-bs-theme', currentTheme === 'dark' ? 'light' : 'dark');
  }
}
