package com.library.catalog.client;

import com.library.catalog.dto.BookDTO;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Component
public class LibraryApiClientFallback implements LibraryApiClient {

    private static final Logger log = LoggerFactory.getLogger(LibraryApiClientFallback.class);

    @Override
    public BookDTO getBookById(Long id) {
        log.warn("Fallback: Library API unavailable. Returning placeholder for book ID: {}", id);
        return BookDTO.builder()
                .id(id)
                .title("Unavailable")
                .author("Unavailable")
                .isbn("N/A")
                .build();
    }
}
