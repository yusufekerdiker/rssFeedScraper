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

  //handle alert message when article added to or removed from favorites
  @Output() alertEmitter = new EventEmitter<{
    message: string;
    type: string;
  }>();

  isFavorite: boolean = false;

  constructor(private newsService: NewsService) {}

  ngOnInit(): void {
    //check if the article is already favorited
    this.isFavorite = this.newsService.isFavorite(this.article);
  }

  toggleFavorite() {
    //check the current favorite state of the article and toggle it
    if (this.isFavorite) {
      //use the newsService to remove it from favorites
      this.newsService.removeFromFavorites(this.article);
      //emit an event to show an alert that the article has been removed from favorites
      this.alertEmitter.emit({
        message: 'Article removed from favorites',
        type: 'danger',
      });
    } else {
      //if the article is not favorited, use the newsService to add it to favorites
      this.newsService.addToFavorites(this.article);
      // show an alert for article has been added
      this.alertEmitter.emit({
        message: 'Article added to favorites',
        type: 'success',
      });
    }
    this.isFavorite = !this.isFavorite;
  }
}
