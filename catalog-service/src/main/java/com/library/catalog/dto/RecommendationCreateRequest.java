package com.library.catalog.dto;

import jakarta.validation.constraints.*;
import lombok.*;

@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class RecommendationCreateRequest {

    @NotNull(message = "Book ID is required")
    private Long bookId;

    @NotBlank(message = "Recommender name is required")
    private String recommendedBy;

    private String reason;

    @NotNull(message = "Rating is required")
    @Min(value = 1, message = "Rating must be between 1 and 5")
    @Max(value = 5, message = "Rating must be between 1 and 5")
    private Integer rating;
}
