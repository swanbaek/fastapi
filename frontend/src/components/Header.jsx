// Header.jsx
import { Navbar, Container, Nav, NavDropdown } from 'react-bootstrap';
import { Link } from 'react-router-dom';

export default function Header() {
    return (
        <Navbar collapseOnSelect expand="lg" className="bg-body-tertiary" fixed="top" bg="dark" data-bs-theme="dark">
            <Container>
                <Navbar.Brand as={Link} to="/">
                    Best
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="responsive-navbar-nav" />
                <Navbar.Collapse id="responsive-navbar-nav">
                    <Nav className="me-auto">
                        <Nav.Link as={Link} to="/signup">
                            SingUp
                        </Nav.Link>
                        <Nav.Link href="#pricing">SignIn</Nav.Link>
                        <NavDropdown title="Admin" id="collapsible-nav-dropdown">
                            <NavDropdown.Item as={Link} to="/admin/users">
                                회원관리
                            </NavDropdown.Item>
                            <NavDropdown.Item>상품관리</NavDropdown.Item>
                            <NavDropdown.Item>주문관리</NavDropdown.Item>
                            <NavDropdown.Divider />
                            <NavDropdown.Item>Separated link</NavDropdown.Item>
                        </NavDropdown>
                    </Nav>
                    <Nav>
                        <Nav.Link as={Link} to="/posts">
                            Posts
                        </Nav.Link>
                        <Nav.Link eventKey={2} as={Link} to="/mypage">
                            MyPage
                        </Nav.Link>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
}
