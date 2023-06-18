import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Article } from 'src/app/models/news';
import { NewsService } from 'src/app/services/news.service';

@Component({
  selector: 'app-card',
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.scss'],
})
export class CardComponent {
  @Input()
  article!: Article;

  @Output() alertEmitter = new EventEmitter<{
    message: string;
    type: string;
  }>();

  isFavorite: boolean = false;

  constructor(private newsService: NewsService) {}

  ngOnInit(): void {
    this.isFavorite = this.newsService.isFavorite(this.article);
  }

  toggleFavorite() {
    this.isFavorite = this.newsService.isFavorite(this.article);
    if (this.isFavorite) {
      this.newsService.removeFromFavorites(this.article);
      this.alertEmitter.emit({
        message: 'Article removed from favorites',
        type: 'danger',
      });
    } else {
      this.newsService.addToFavorites(this.article);
      this.alertEmitter.emit({
        message: 'Article added to favorites',
        type: 'success',
      });
    }
    this.isFavorite = !this.isFavorite;
  }
}
