package com.library.catalog.dto;

import lombok.*;

import java.time.LocalDate;

@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class RecommendationDTO {
    private Long id;
    private Long bookId;
    private String bookTitle;
    private String bookAuthor;
    private String recommendedBy;
    private String reason;
    private Integer rating;
    private LocalDate createdDate;
}
