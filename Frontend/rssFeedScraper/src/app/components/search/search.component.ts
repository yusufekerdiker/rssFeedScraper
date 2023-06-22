import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Article } from 'src/app/models/news';
import { NewsService } from 'src/app/services/news.service';
import { SearchService } from 'src/app/services/search.service';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss'],
})
export class SearchComponent implements OnInit {
  allNews: Article[] = [];
  filteredNews: Article[] = [];
  searchTerm: string = '';

  constructor(
    private newsService: NewsService,
    private searchService: SearchService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.searchService.getSearchTerm().subscribe((term) => {
      this.searchTerm = term;

      // Clear the existing news data
      this.allNews = [];

      this.newsService.getNews().subscribe((news) => {
        for (let publisher in news) {
          this.allNews.push(...news[publisher]);
        }
        // Filter the news by the search term
        this.filteredNews = this.allNews.filter(
          (article) =>
            article.title.toLowerCase().includes(term.toLowerCase()) ||
            article.description.toLowerCase().includes(term.toLowerCase())
        );
      });
    });
  }
}
