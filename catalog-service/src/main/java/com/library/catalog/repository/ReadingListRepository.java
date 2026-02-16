package com.library.catalog.repository;

import com.library.catalog.entity.ReadingList;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ReadingListRepository extends JpaRepository<ReadingList, Long> {
    List<ReadingList> findByOwnerName(String ownerName);
}
