import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { NewsProviderComponent } from './components/news-provider/news-provider.component';
import { CategoriesComponent } from './components/categories/categories.component';

const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' }, // Redirect to /home by default
  { path: 'home', component: HomeComponent },
  // {path: 'cards', loadChildren: () => import('./cards/cards.module').then(m => m.CardsModule)} // lazy loading
  { path: 'publisher/:publisher', component: NewsProviderComponent },
  { path: 'categories', component: CategoriesComponent },


];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
