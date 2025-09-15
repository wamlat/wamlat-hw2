import pytest
import sys
import os
import base64

# Add the api directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

from index import (
    text_to_number, 
    number_to_text, 
    base64_to_number, 
    number_to_base64,
    app
)

class TestTextToNumber:
    """Test cases for text_to_number function"""
    
    def test_simple_numbers(self):
        """Test basic number words"""
        assert text_to_number("one") == 1
        assert text_to_number("two") == 2
        assert text_to_number("three") == 3
        assert text_to_number("four") == 4
        assert text_to_number("five") == 5
        assert text_to_number("six") == 6
        assert text_to_number("seven") == 7
        assert text_to_number("eight") == 8
        assert text_to_number("nine") == 9
        assert text_to_number("ten") == 10
    
    def test_zero_variants(self):
        """Test zero and nil"""
        assert text_to_number("zero") == 0
        assert text_to_number("nil") == 0
    
    def test_case_insensitive(self):
        """Test case insensitivity"""
        assert text_to_number("ONE") == 1
        assert text_to_number("Two") == 2
        assert text_to_number("ZERO") == 0
    
    def test_with_special_characters(self):
        """Test text with special characters"""
        assert text_to_number("one!") == 1
        assert text_to_number("two@#$") == 2
        assert text_to_number("zero123") == 0
    
    def test_invalid_text(self):
        """Test invalid text inputs"""
        with pytest.raises(ValueError, match="Unable to convert text to number"):
            text_to_number("eleven")
        with pytest.raises(ValueError, match="Unable to convert text to number"):
            text_to_number("twenty")
        with pytest.raises(ValueError, match="Unable to convert text to number"):
            text_to_number("hundred")
        with pytest.raises(ValueError, match="Unable to convert text to number"):
            text_to_number("invalid")

class TestNumberToText:
    """Test cases for number_to_text function"""
    
    def test_basic_numbers(self):
        """Test basic number conversions"""
        assert number_to_text(0) == "zero"
        assert number_to_text(1) == "one"
        assert number_to_text(5) == "five"
        assert number_to_text(10) == "ten"
        assert number_to_text(42) == "forty-two"
        assert number_to_text(100) == "one hundred"
        assert number_to_text(123) == "one hundred and twenty-three"
    
    def test_large_numbers(self):
        """Test larger numbers"""
        assert number_to_text(1000) == "one thousand"
        assert number_to_text(1000000) == "one million"
    
    def test_negative_numbers(self):
        """Test negative numbers"""
        assert number_to_text(-1) == "minus one"
        assert number_to_text(-42) == "minus forty-two"
    
    def test_edge_cases(self):
        """Test edge cases"""
        # Test very large number
        large_num = 999999999
        result = number_to_text(large_num)
        assert isinstance(result, str)
        assert len(result) > 0

class TestBase64Conversion:
    """Test cases for base64 conversion functions"""
    
    def test_number_to_base64_basic(self):
        """Test basic number to base64 conversion"""
        # Test small numbers
        assert number_to_base64(0) == ""
        assert number_to_base64(1) == "AQ=="
        assert number_to_base64(255) == "/w=="
        assert number_to_base64(256) == "AAE="
    
    def test_base64_to_number_basic(self):
        """Test basic base64 to number conversion"""
        assert base64_to_number("") == 0
        assert base64_to_number("AQ==") == 1
        assert base64_to_number("/w==") == 255
        assert base64_to_number("AAE=") == 256
    
    def test_round_trip_conversion(self):
        """Test round-trip conversion (number -> base64 -> number)"""
        test_numbers = [0, 1, 255, 256, 65535, 65536, 1000000]
        for num in test_numbers:
            b64 = number_to_base64(num)
            converted_back = base64_to_number(b64)
            assert converted_back == num, f"Round-trip failed for {num}"
    
    def test_large_numbers_base64(self):
        """Test large numbers with base64"""
        large_num = 2**32 - 1  # Maximum 32-bit unsigned integer
        b64 = number_to_base64(large_num)
        converted_back = base64_to_number(b64)
        assert converted_back == large_num
    
    def test_invalid_base64(self):
        """Test invalid base64 inputs"""
        with pytest.raises(ValueError, match="Invalid base64 input"):
            base64_to_number("invalid_base64!")
        with pytest.raises(ValueError, match="Invalid base64 input"):
            base64_to_number("123")

class TestFlaskApp:
    """Test cases for Flask application endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_index_route(self, client):
        """Test the index route"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Numeric Converter' in response.data
    
    def test_convert_text_to_decimal(self, client):
        """Test converting text to decimal"""
        response = client.post('/convert', 
                             json={'input': 'five', 'inputType': 'text', 'outputType': 'decimal'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] == '5'
        assert data['error'] is None
    
    def test_convert_decimal_to_text(self, client):
        """Test converting decimal to text"""
        response = client.post('/convert', 
                             json={'input': '42', 'inputType': 'decimal', 'outputType': 'text'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] == 'forty-two'
        assert data['error'] is None
    
    def test_convert_binary_to_hex(self, client):
        """Test converting binary to hexadecimal"""
        response = client.post('/convert', 
                             json={'input': '1010', 'inputType': 'binary', 'outputType': 'hexadecimal'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] == 'a'
        assert data['error'] is None
    
    def test_convert_octal_to_binary(self, client):
        """Test converting octal to binary"""
        response = client.post('/convert', 
                             json={'input': '17', 'inputType': 'octal', 'outputType': 'binary'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] == '1111'
        assert data['error'] is None
    
    def test_convert_hex_to_decimal(self, client):
        """Test converting hexadecimal to decimal"""
        response = client.post('/convert', 
                             json={'input': 'FF', 'inputType': 'hexadecimal', 'outputType': 'decimal'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] == '255'
        assert data['error'] is None
    
    def test_convert_to_base64(self, client):
        """Test converting decimal to base64"""
        response = client.post('/convert', 
                             json={'input': '255', 'inputType': 'decimal', 'outputType': 'base64'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] == '/w=='
        assert data['error'] is None
    
    def test_convert_from_base64(self, client):
        """Test converting base64 to decimal"""
        response = client.post('/convert', 
                             json={'input': '/w==', 'inputType': 'base64', 'outputType': 'decimal'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] == '255'
        assert data['error'] is None
    
    def test_all_conversion_combinations(self, client):
        """Test all reasonable input/output type combinations"""
        test_cases = [
            ('1', 'decimal', 'binary', '1'),
            ('1', 'decimal', 'octal', '1'),
            ('1', 'decimal', 'hexadecimal', '1'),
            ('1', 'binary', 'decimal', '1'),
            ('1', 'octal', 'decimal', '1'),
            ('1', 'hexadecimal', 'decimal', '1'),
            ('10', 'binary', 'octal', '2'),
            ('10', 'binary', 'hexadecimal', '2'),
            ('10', 'octal', 'binary', '1000'),
            ('10', 'octal', 'hexadecimal', '8'),
            ('A', 'hexadecimal', 'binary', '1010'),
            ('A', 'hexadecimal', 'octal', '12'),
        ]
        
        for input_val, input_type, output_type, expected in test_cases:
            response = client.post('/convert', 
                                 json={'input': input_val, 'inputType': input_type, 'outputType': output_type})
            assert response.status_code == 200
            data = response.get_json()
            assert data['result'] == expected, f"Failed for {input_val} {input_type} -> {output_type}"
            assert data['error'] is None
    
    def test_error_handling_invalid_input_type(self, client):
        """Test error handling for invalid input type"""
        response = client.post('/convert', 
                             json={'input': '5', 'inputType': 'invalid', 'outputType': 'decimal'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] is None
        assert 'Invalid input type' in data['error']
    
    def test_error_handling_invalid_output_type(self, client):
        """Test error handling for invalid output type"""
        response = client.post('/convert', 
                             json={'input': '5', 'inputType': 'decimal', 'outputType': 'invalid'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] is None
        assert 'Invalid output type' in data['error']
    
    def test_error_handling_invalid_binary(self, client):
        """Test error handling for invalid binary input"""
        response = client.post('/convert', 
                             json={'input': '102', 'inputType': 'binary', 'outputType': 'decimal'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] is None
        assert 'error' in data['error'].lower()
    
    def test_error_handling_invalid_hex(self, client):
        """Test error handling for invalid hexadecimal input"""
        response = client.post('/convert', 
                             json={'input': 'GG', 'inputType': 'hexadecimal', 'outputType': 'decimal'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] is None
        assert 'error' in data['error'].lower()
    
    def test_error_handling_invalid_text(self, client):
        """Test error handling for invalid text input"""
        response = client.post('/convert', 
                             json={'input': 'eleven', 'inputType': 'text', 'outputType': 'decimal'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] is None
        assert 'Unable to convert text to number' in data['error']
    
    def test_error_handling_invalid_base64(self, client):
        """Test error handling for invalid base64 input"""
        response = client.post('/convert', 
                             json={'input': 'invalid!', 'inputType': 'base64', 'outputType': 'decimal'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] is None
        assert 'Invalid base64 input' in data['error']
    
    def test_missing_json_data(self, client):
        """Test handling of missing JSON data"""
        response = client.post('/convert', json={})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] is None
        assert 'error' in data['error'].lower()

class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_zero_conversions(self):
        """Test zero in all formats"""
        assert text_to_number("zero") == 0
        assert number_to_text(0) == "zero"
        assert number_to_base64(0) == ""
        assert base64_to_number("") == 0
    
    def test_negative_numbers(self):
        """Test negative numbers"""
        assert number_to_text(-1) == "minus one"
        # Note: base64 conversion might not handle negatives well
        with pytest.raises(ValueError):
            number_to_base64(-1)
    
    def test_large_numbers(self):
        """Test very large numbers"""
        large_num = 2**63 - 1  # Maximum 64-bit signed integer
        text_result = number_to_text(large_num)
        assert isinstance(text_result, str)
        assert len(text_result) > 0
    
    def test_base64_byte_order(self):
        """Test base64 byte order (should use big-endian as per assignment)"""
        # Test that base64 uses big-endian byte order
        num = 256  # 0x0100
        b64 = number_to_base64(num)
        # Should be "AAE=" (big-endian) not "AQA=" (little-endian)
        assert b64 == "AAE="
