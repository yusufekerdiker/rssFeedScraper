import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatSelectChange } from '@angular/material/select';
import { Observable, filter } from 'rxjs';
import { Article, News } from 'src/app/models/news';
import { NewsService } from 'src/app/services/news.service';

@Component({
  selector: 'app-deneme',
  templateUrl: './deneme.component.html',
  styleUrls: ['./deneme.component.scss']
})
export class DenemeComponent implements OnInit {
  allNews!: Observable<News>;
  allCategories: {name: string, count: number}[] = [];
  selectedCategories: Set<string> = new Set();
  filteredNews: Article[] = [];
  searchTerm: string = '';
  searchControl = new FormControl('');

  constructor(private newsService: NewsService) {
    this.searchControl.valueChanges.pipe(
      filter(value => value !== null)
    ).subscribe(value => {
      this.searchTerm = value as string;
      this.filterNews();
    });
   }

   ngOnInit(): void {
    this.allNews = this.newsService.getNews();
    this.allNews.subscribe(news => {
      const categoryCounts: { [category: string]: number } = {};
      for (let publisher in news) {
        news[publisher].forEach(article => {
          article.categories.forEach(category => {
            if (category in categoryCounts) {
              categoryCounts[category]++;
            } else {
              categoryCounts[category] = 1;
            }
          });
        });
      }
      this.allCategories = Object.entries(categoryCounts).map(([name, count]) => ({name, count}));
      this.filterNews();
    });
  }
  

  filterNews(): void {
    this.filteredNews = [];
    this.allNews.subscribe(news => {
      for (let publisher in news) {
        news[publisher].forEach(article => {
          if ((article.categories.some(category => this.selectedCategories.has(category))) 
            && (article.title.toLowerCase().includes(this.searchTerm.toLowerCase()) 
            || article.description.toLowerCase().includes(this.searchTerm.toLowerCase()))) {
              this.filteredNews.push(article);
          }
        });
      }
    });
  }

  getCategories(): void {
    this.allNews.subscribe(news => {
      const categoryCounts: { [category: string]: number } = {};
      for (let publisher in news) {
        news[publisher].forEach(article => {
          article.categories.forEach(category => {
            if (category in categoryCounts) {
              categoryCounts[category]++;
            } else {
              categoryCounts[category] = 1;
            }
          });
        });
      }
      this.allCategories = Object.entries(categoryCounts).map(([name, count]) => ({name, count}));
    });
  }
  
  updateFilter(event: MatSelectChange): void {
    // event.value is an array of the selected category objects
    // Extract the name property of each object to get the category names
    this.selectedCategories = new Set(event.value.map((category: { name: string; }) => category.name));
    this.filterNews();
  }
  
  

}