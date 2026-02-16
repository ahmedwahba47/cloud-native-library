package com.library.catalog.dto;

import lombok.*;

import java.time.LocalDate;
import java.util.List;

@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class ReadingListDTO {
    private Long id;
    private String name;
    private String description;
    private String ownerName;
    private LocalDate createdDate;
    private List<ReadingListItemDTO> items;
}
