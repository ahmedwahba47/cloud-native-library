package com.library.catalog.dto;

import jakarta.validation.constraints.NotNull;
import lombok.*;

@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class AddBookRequest {

    @NotNull(message = "Book ID is required")
    private Long bookId;

    private String notes;
}
