import { Component, OnInit } from '@angular/core';
import { NewsService } from '../../services/news.service';
import { Article } from '../../models/news';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-categories',
  templateUrl: './categories.component.html',
  styleUrls: ['./categories.component.scss'],
})
export class CategoriesComponent implements OnInit {
  allArticles: Article[] = [];
  filteredArticles: Article[] = [];
  selectedCategories = new FormControl();
  categories: string[] = [];
  categoryCountMap: Map<string, number> = new Map<string, number>();

  constructor(private newsService: NewsService) { }

  ngOnInit(): void {
    this.newsService.getNews().subscribe((data: { [key: string]: Article[] }) => {
      for (const publisher in data) {
        this.allArticles = this.allArticles.concat(data[publisher]);
      }
      this.generateCategoryList();
      this.generateCategoryCountMap();
    });
  }

  generateCategoryList(): void {
    const categorySet = new Set<string>();
    this.allArticles.forEach(article => {
      article.categories.forEach(category => {
        categorySet.add(category);
      });
    });
    this.categories = Array.from(categorySet);
  }

  generateCategoryCountMap(): void {
    this.allArticles.forEach(article => {
      article.categories.forEach(category => {
        if (!this.categoryCountMap.has(category)) {
          this.categoryCountMap.set(category, 1);
        } else {
          this.categoryCountMap.set(category, this.categoryCountMap.get(category) as number + 1);
        }
      });
    });
  }

  onSelectionChange(): void {
    let selected = this.selectedCategories.value;
    this.filteredArticles = this.allArticles.filter(article =>
      article.categories.some(category => selected.includes(category))
    );
  }

  isArticleInArray(article: Article, array: Article[]): boolean {
    return array.some(a => a.title === article.title && a.link === article.link);
  }
}