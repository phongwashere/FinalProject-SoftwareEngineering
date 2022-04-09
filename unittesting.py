"""
unit tests
"""
import unittest
from spotifyapi import search, recommendedartist, categoryplaylist, gettracks


class Spotifytest(unittest.TestCase):
    """unit tests"""

    def test_search(self):
        """testing search for expected output"""
        test_song = "cardigan"
        expected_output = "06HL4z0CvFAxyc27GXpf02"
        actual_output = search(test_song)
        self.assertEqual(expected_output, actual_output)

    def test_search_none(self):
        """testing search for expected output"""
        test_song = None
        expected_output = "invalid song"
        actual_output = search(test_song)
        self.assertEqual(expected_output, actual_output)

    def test_search_wrong(self):
        """test for entering a song that doesn't exist"""
        testing_none = "jhvuydcityxdiytd"
        expected_output = None
        actual_output = search(testing_none)
        self.assertEqual(expected_output, actual_output)

    def test_recommendedartist(self):
        """testing functionality for recommededArtist"""
        test_id = "06HL4z0CvFAxyc27GXpf02"  # spotift api may change the expected output later in the future
        expected_output = [
            "Demi Lovato",
            "Alessia Cara",
            "Lorde",
            "Selena Gomez",
            "Troye Sivan",
            "ZAYN",
            "Harry Styles",
            "Niall Horan",
            "Miley Cyrus",
            "Camila Cabello",
        ]
        actual_output = recommendedartist(test_id)
        self.assertEqual(expected_output, actual_output)

    def test_categoryplaylist(self):
        """test if categoryplaylist returns a playlist id"""
        test_id = "pop"
        expected_output = "37i9dQZF1DXcBWIGoYBM5M"
        actual_output = categoryplaylist(test_id)
        self.assertEqual(expected_output, actual_output)

    def test_invalid_gettracks(self):
        """test if get tracks returns invalid id"""
        test_id = "adshfupaewgfaipue12"
        expected_output = "invalid id"
        actual_output = gettracks(test_id)
        self.assertEqual(expected_output, actual_output)


if __name__ == "__main__":
    unittest.main()
