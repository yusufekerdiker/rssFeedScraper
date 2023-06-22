import { Component } from '@angular/core';
import { Article } from 'src/app/models/news';
import { NewsService } from 'src/app/services/news.service';

@Component({
  selector: 'app-favorites',
  templateUrl: './favorites.component.html',
  styleUrls: ['./favorites.component.scss'],
})
export class FavoritesComponent {
  favorites: Article[] = [];

  constructor(private newsService: NewsService) {}

  ngOnInit(): void {
    this.favorites = this.newsService.getFavorites();
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
