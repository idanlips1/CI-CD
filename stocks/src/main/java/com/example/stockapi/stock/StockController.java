package com.example.stockapi.stock;

import java.util.*;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestClientException;

@RestController

public class StockController {

    private final StockService stockService;

    @Autowired
    public StockController(StockService stockService) {
        this.stockService = stockService;

    }

    @PostMapping("/stocks")
    public ResponseEntity<Map<String, String>> addStock(@RequestBody Stock stock) {
        try {
            if (!stock.isPostValid()) {
                return new ResponseEntity<>(Map.of("error", "Malformed data"),
                        HttpStatus.BAD_REQUEST);
            }
            List<Stock> temp = stockService.getAllStocks();
            for (int i = 0; i < temp.size(); i++) {
                if (stock.getSymbol().equals(temp.get(i).getSymbol())) {
                    return new ResponseEntity<>(Map.of("error", "Malformed data"), HttpStatus.BAD_REQUEST);
                }
            }
            String id = stockService.addToMap(stock);
            return new ResponseEntity<>(Map.of("id", id), HttpStatus.CREATED);
        } catch (Exception e) {
            Map<String, String> errorResponse = Map.of("server error", e.getMessage());
            return new ResponseEntity<>(errorResponse, HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/stocks/{id}")
    public ResponseEntity getStockById(@PathVariable String id) {
        try {
            Stock stock = stockService.getStock(id);

            if (stock == null) {
                Map<String, String> errorResponse = Map.of("error", "Not found");
                return new ResponseEntity<>(errorResponse, HttpStatus.NOT_FOUND);
            }
            return new ResponseEntity<>(stock, HttpStatus.OK);
        } catch (Exception e) {
            Map<String, String> errorResponse = Map.of("server error", e.getMessage());
            return new ResponseEntity<>(errorResponse, HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/stocks")
    public ResponseEntity getStocks(
        @RequestParam(required = false) String symbol,
        @RequestParam(required = false) String name,
        @RequestParam(required = false) Float purchase_price,
        @RequestParam(required = false) String purchase_date,
        @RequestParam(required = false) Integer shares
    ) {
        try {
            Map<String, Object> filters = new HashMap<>();
            if (symbol != null) filters.put("symbol", symbol);
            if (name != null) filters.put("name", name);
            if (purchase_price != null) filters.put("purchase_price", purchase_price);
            if (purchase_date != null) filters.put("purchase_date", purchase_date);
            if (shares != null) filters.put("shares", shares);

            if (filters.isEmpty()) {
                return new ResponseEntity<>(stockService.getAllStocks(), HttpStatus.OK);
            }
            return new ResponseEntity<>(stockService.getStocksWithFilters(filters), HttpStatus.OK);
        } catch (Exception e) {
            Map<String, String> errorResponse = Map.of("server error", e.getMessage());
            return new ResponseEntity<>(errorResponse, HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @DeleteMapping("/stocks/{id}")
    public ResponseEntity deleteStockbyID(@PathVariable String id) {
        try {
            Stock stock = stockService.getStock(id);
            if (stock == null) {
                return new ResponseEntity<>(HttpStatus.NOT_FOUND);

            }
            stockService.deleteById(id);
            return new ResponseEntity<>(HttpStatus.NO_CONTENT);

        } catch (Exception e) {
            Map<String, String> errorResponse = Map.of("server error", e.getMessage());
            return new ResponseEntity<>(errorResponse, HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @PutMapping("/stocks/{id}")
    public ResponseEntity updateGivenStock(@PathVariable String id, @RequestBody Stock stock) {
        try {
            if (stock == null || stock.getId() == null || stock.getId().isEmpty()) {
                return new ResponseEntity<>(Map.of("error", "Malformed data"), HttpStatus.BAD_REQUEST);
            }
            if (!stock.isStockValid()) {
                return new ResponseEntity<>(Map.of("error", "Expected application/json media type"),
                        HttpStatus.UNSUPPORTED_MEDIA_TYPE);

            }
            Stock existingStock = stockService.getStock(id);
            if (existingStock == null) {
                Map<String, String> errorResponse = Map.of("error", "Not found");
                return new ResponseEntity<>(errorResponse, HttpStatus.NOT_FOUND);
            }
            stockService.updateStock(stock);
            return new ResponseEntity<>(HttpStatus.OK);

        } catch (Exception e) {
            Map<String, String> errorResponse = Map.of("server error", e.getMessage());
            return new ResponseEntity<>(errorResponse, HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/stock-value/{id}")
    public ResponseEntity getStockValue(@PathVariable String id) {

        try {
            Stock stock = stockService.getStock(id);
            if (stock == null) {
                return new ResponseEntity<>(HttpStatus.NOT_FOUND);
            }

            return new ResponseEntity<>(stockService.getStockValue(id), HttpStatus.OK);
        } catch (Exception e) {
            Map<String, String> errorResponse = Map.of("server error", e.getMessage());
            return new ResponseEntity<>(errorResponse, HttpStatus.INTERNAL_SERVER_ERROR);
        }

    }

    @GetMapping("/portfolio-value")
    public ResponseEntity getPortfolioValue() {
        try {
            PortfolioValueResponse portfolioValue = stockService.getPortfolio();
            return new ResponseEntity<>(portfolioValue, HttpStatus.OK);
        } catch (Exception e) {
            Map<String, String> errorResponse = Map.of("server error", e.getMessage());
            return new ResponseEntity<>(errorResponse, HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/kill")
    public void kill() {
        System.exit(1);
    }
}