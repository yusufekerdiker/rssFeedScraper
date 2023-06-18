import { Pipe, PipeTransform } from '@angular/core';
import { Article } from '../models/news';

@Pipe({
  name: 'categoryFilter'
})
export class CategoryFilterPipe implements PipeTransform {

  transform(items: Article[], selectedCategory: string): Article[] {
    if (!items || !selectedCategory) {
      return items;
    }
    return items.filter(item => item.categories.includes(selectedCategory));
  }
}
