import { Component, EventEmitter, Output } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Router } from '@angular/router';
import { SearchService } from 'src/app/services/search.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent {

  publishers: string[] = ['CNET', 'Wired'];

  showSearch = false;
  isDarkTheme: boolean = false;

  searchTerm = new FormControl('');

  constructor(private searchService: SearchService, private router: Router) { }

  onSearch(event: Event): void {
    event.preventDefault();  // prevent the default form submission behaviour
    console.log("onSearch() called");
    const term = this.searchTerm.value || '';
    this.searchService.setSearchTerm(term);
    if (term) {
      this.router.navigate(['/search', term]);
    } else {
      this.router.navigate(['/home']);
    }
  } 

  toggleSearch() {
    this.showSearch = !this.showSearch;
  }

  @Output() themeSwitch = new EventEmitter<void>();

  switchTheme(): void {
    const currentTheme = document.documentElement.getAttribute('data-theme');

    this.isDarkTheme = currentTheme === 'dark';

    const newTheme = this.isDarkTheme ? 'light' : 'dark';

    // Switch bootstrap theme
    document.documentElement.setAttribute('data-bs-theme', newTheme);

    // Emit to switch angulatmat theme
    this.themeSwitch.emit();
  }
}
