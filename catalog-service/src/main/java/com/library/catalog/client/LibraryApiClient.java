package com.library.catalog.client;

import com.library.catalog.dto.BookDTO;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@FeignClient(name = "library-api", fallback = LibraryApiClientFallback.class)
public interface LibraryApiClient {

    @GetMapping("/api/books/{id}")
    BookDTO getBookById(@PathVariable("id") Long id);
}
