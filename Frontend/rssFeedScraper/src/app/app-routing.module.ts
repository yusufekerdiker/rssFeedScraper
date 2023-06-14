import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';

const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' }, // Redirect to /home by default
  { path: 'home', component: HomeComponent },
  // {path: 'cards', loadChildren: () => import('./cards/cards.module').then(m => m.CardsModule)} // lazy loading

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
