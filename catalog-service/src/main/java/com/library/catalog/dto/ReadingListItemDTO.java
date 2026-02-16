package com.library.catalog.dto;

import lombok.*;

import java.time.LocalDate;

@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class ReadingListItemDTO {
    private Long id;
    private Long bookId;
    private String bookTitle;
    private String bookAuthor;
    private LocalDate addedDate;
    private String notes;
    private String readStatus;
}
